from fastapi import FastAPI

app = FastAPI(
    title="ManagePhoto",
    description="FastAPI Cognito API authentication service",
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]
)
