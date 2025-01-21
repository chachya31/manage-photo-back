from fastapi import APIRouter, Form, status, Depends
from pydantic import EmailStr
from domain.entity.user import UserEmail, UserSignUp, UserVerify, UserSignIn, ConfirmForgotPassword, ChangePassword, RefreshToken, AccessToken
from usecase.service.auth_service import AuthService
from core.aws_cognito import AWS_Cognito
from core.dependencies import get_aws_cognito



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
@auth_router.get("/user_detail", status_code=status.HTTP_200_OK, tags=["Auth"])
async def user_details(
    email: EmailStr = Form(),
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.user_details(email, cognito)


@auth_router.get("/list", status_code=status.HTTP_200_OK, tags=["Auth"])
async def list_user(
    cognito: AWS_Cognito = Depends(get_aws_cognito)
):
    return AuthService.list_user(cognito)

