import uvicorn
from middleware.exception_handler import EnhancedTracebackMiddleware

from init import app
from controller.auth import auth_router

app = app
# ミドルウェア登録
app.add_middleware(EnhancedTracebackMiddleware)


@app.get("/")
def index():
    return {"message": "Authentication service"}


app.include_router(auth_router)

# デバッグ
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
