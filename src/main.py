import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from middleware.exception_handler import EnhancedTracebackMiddleware

from init import app
from controller.auth import auth_router

app = app
# ミドルウェア登録
app.add_middleware(EnhancedTracebackMiddleware)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Authentication service"}


app.include_router(auth_router)

# デバッグ
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
