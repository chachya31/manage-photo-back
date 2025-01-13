from fastapi import APIRouter, Form, status, Depends, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr
from typing import Dict, List, Optional

import requests

from core.JWTBearer import JWTBearer
from domain.entity.user import UserEmail, UserSignUp, UserVerify, UserSignIn, ConfirmForgotPassword, ChangePassword, RefreshToken, AccessToken
from usecase.service.auth_service import AuthService
from core.aws_cognito import AWS_Cognito
from core.dependencies import get_aws_cognito
from core.jwt import jwks, get_current_user

from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode



from core.config import env_vars

AWS_REGION_NAME = env_vars.AWS_REGION_NAME
AWS_COGNITO_APP_CLIENT_ID = env_vars.AWS_COGNITO_APP_CLIENT_ID
AWS_COGNITO_USER_POOL_ID = env_vars.AWS_COGNITO_USER_POOL_ID

auth_router = APIRouter(prefix="/api/v1/auth")


# ユーザ登録
@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def signup_user(
    user: UserSignUp,
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.user_signup(user, cognito)


# メールアドレス認証
@auth_router.post("/verify_account", status_code=status.HTTP_200_OK, tags=["Auth"])
async def verify_account(
    data: UserVerify,
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.verify_account(data, cognito)


# 認証コード再送信申請
@auth_router.post("/resend_confirmation_code", status_code=status.HTTP_200_OK, tags=["Auth"])
async def resend_confirmation_code(
    data: UserEmail = Form(...),
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.resend_confirmation_code(data.email, cognito)


# ログイン
@auth_router.post("/signin", status_code=status.HTTP_200_OK, tags=["Auth"])
async def signin(
    data: UserSignIn,
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.user_signin(data, cognito)


# パスワード忘れ：再発行申請
@auth_router.post("/forgot_password", status_code=status.HTTP_200_OK, tags=["Auth"])
async def forgot_password(
    data: UserEmail,
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.forgot_password(data.email, cognito)


# パスワード忘れ：パスワード変更
@auth_router.post("/confirm_forgot_password", status_code=status.HTTP_200_OK, tags=["Auth"])
async def confirm_forgot_password(
    data: ConfirmForgotPassword,
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.confirm_forgot_password(data, cognito)


# パスワード変更
@auth_router.post("/change_password", status_code=status.HTTP_200_OK, tags=["Auth"])
async def change_password(
    data: ChangePassword,
    cognito: AWS_Cognito = Depends(get_aws_cognito),
):
    return AuthService.change_password(data, cognito)


# アクセストークン再発行
@auth_router.post("/new_token", status_code=status.HTTP_200_OK, tags=["Auth"])
async def new_access_token(
    refresh_token: RefreshToken,
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.new_access_token(refresh_token.refresh_token, cognito)


# ログアウト
@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["Auth"])
async def logout(
    access_token: AccessToken,
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.logout(access_token.access_token, cognito)


# ユーザ情報取得
@auth_router.get("/user_details", status_code=status.HTTP_200_OK, tags=["Auth"])
async def user_detail(
    email: EmailStr,
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.user_details(email, cognito)

auth = JWTBearer(jwks)

@auth_router.get("/test")
async def test(username: str = Depends(get_current_user)):
    return {"username": username}

@auth_router.get("/secure", dependencies=[Depends(auth)])
async def secure() -> bool:
    return True

@auth_router.get("/not_secure")
async def not_secure() -> bool:
    return True





JWK = Dict[str, str]
JWKS = Dict[str, List[JWK]]

def get_jwks() -> JWKS:
    return requests.get(f"https://cognito-idp.{AWS_REGION_NAME}.amazonaws.com/{AWS_COGNITO_USER_POOL_ID}/.well-known/jwks.json"
                        ).json()

@auth_router.get("/jwk", status_code=status.HTTP_200_OK, tags=["Auth"])
async def test():
    return get_jwks()

SECRET_KEY = "XubcZ7xUyc3RPQk1ckFuWVnKABapAKLl74S3+zCI"
ALGORITHM = "RS256"

security = HTTPBearer()

def get_current_users(
    token: HTTPAuthorizationCredentials = Security(security)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token or expired token")

@auth_router.get("/", status_code=status.HTTP_200_OK, tags=["Auth"])
def read_protected(
    user_id: str = Depends(get_current_users)
):
    return { "user_id": user_id }

# @auth_router.get("/", status_code=status.HTTP_200_OK, tags=["Auth"])
# async def verify_token()

