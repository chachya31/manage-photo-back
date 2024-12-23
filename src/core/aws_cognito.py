import boto3
import logging

from pydantic import EmailStr
from domain.entity.user import UserSignUp, UserSignIn, UserVerify, ChangePassword, ConfirmForgotPassword
from .config import env_vars

AWS_REGION_NAME = env_vars.AWS_REGION_NAME
AWS_COGNITO_APP_CLIENT_ID = env_vars.AWS_COGNITO_APP_CLIENT_ID
AWS_COGNITO_USER_POOL_ID = env_vars.AWS_COGNITO_USER_POOL_ID


class AWS_Cognito:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=AWS_REGION_NAME)

    # ユーザ登録
    def user_signup(self, user: UserSignUp):
        response = self.client.sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=user.email,
            Password=user.password,
            UserAttributes=[
                {
                    "Name": "name",
                    "Value": user.full_name
                },
                {
                    "Name": "phone_number",
                    "Value": user.phone_number
                },
                {
                    "Name": "custom:role",
                    "Value": user.role
                },
            ]
        )

        return response

    # ユーザ認証
    def verify_account(self, data: UserVerify):
        response = self.client.confirm_sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.confirmation_code,
        )
        return response

    # 認証コード再送信
    def resend_confirmation_code(self, email: EmailStr):
        response = self.client.resend_confirmation_code(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=email
        )
        return response

    # ユーザ存在チェック
    def check_user_exists(self, email: EmailStr):
        response = self.client.admin_get_user(
            UserPoolId=AWS_COGNITO_USER_POOL_ID,
            Username=email
        )
        return response

    # ログイン
    def user_signin(self, data: UserSignIn):
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": data.email,
                "PASSWORD": data.password
            }
        )
        return response

    # パスワード忘れ：再発行申請
    def forgot_password(self, email: EmailStr):
        response = self.client.forgot_password(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=email
        )
        return response

    # パスワード忘れ：パスワード変更
    def confirm_forgot_password(self, data: ConfirmForgotPassword):
        response = self.client.confirm_forgot_password(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.confirmation_code,
            Password=data.new_password
        )
        return response

    # パスワード変更
    def change_password(self, data: ChangePassword):
        response = self.client.change_password(
            PreviousPassword=data.old_password,
            ProposedPassword=data.new_password,
            AccessToken=data.access_token
        )
        return response

    # アクセストークン再発行
    def new_access_token(self, refresh_token: str):
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
            }
        )
        return response

    # ログアウト
    def logout(self, access_token: str):
        response = self.client.global_sign_out(
            AccessToken=access_token
        )
        return response
