from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from init import app
from schema.response.error_response import ErrorJsonResponse
from core.logging import log_error, get_error_message
from core.config import env_vars

# 環境設定取得
app_env = env_vars.APP_ENV


# カスタムHTTPエラーハンドラ
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    log_error(f"An error occurred: {exc}")
    if app_env == "production":
        error_detail = "Internal Server Error"
    else:
        error_detail = exc.detail
    error = ErrorJsonResponse(
        detail=[
            {
                "loc": [f"{request.method} {request.url.path}"],
                "msg": error_detail,
                "type": "http_error"
            }
        ]
    )
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


class EnhancedTracebackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            log_error(exc)

            # 本番環境ではスタックトレースをレスポンスに含めない
            if app_env == "production":
                error_detail = "Internal Server Error"
            else:
                error_detail = get_error_message(exc)
            error = ErrorJsonResponse(
                detail=[
                    {
                        "loc": [f"{request.method} {request.url.path}"],
                        "msg": error_detail,
                        "type": "server_error",
                    }
                ]
            )
            return JSONResponse(status_code=500, content=error.model_dump())
