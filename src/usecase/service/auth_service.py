import botocore.exceptions
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import botocore
import logging
from pydantic import EmailStr

from core.aws_cognito import AWS_Cognito
from domain.entity.user import UserSignUp, UserVerify, UserSignIn, ConfirmForgotPassword, ChangePassword


class AuthService:
    def user_signup(user: UserSignUp, cognito: AWS_Cognito):
        """ユーザ登録

        Args:
            user (UserSignUp): ユーザ登録フォーム
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.user_signup(user)
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            if e.response["Error"]["Code"] == "UsernameExistsException":
                raise HTTPException(status_code=409, detail="An account with the given email already exists")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                content = {
                    "message": "User created successfully",
                    "sub": response["UserSub"]
                }
                return JSONResponse(content=content, status_code=201)

    def verify_account(data: UserVerify, cognito: AWS_Cognito):
        """ユーザ認証

        Args:
            data (UserVerify): ユーザ認証フォーム
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.verify_account(data)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "CodeMismatchException":
                raise HTTPException(
                    status_code=400, detail="The provided code does not match the expected value."
                )
            elif e.response["Error"]["Code"] == "ExpiredCodeException":
                raise HTTPException(
                    status_code=400, detail="The provided code has expired."
                )
            elif e.response["Error"]["Code"] == "UserNotFoundException":
                raise HTTPException(
                    status_code=404, detail="User not found"
                )
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise HTTPException(
                    status_code=200, detail="User already verified."
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return JSONResponse(content={"message": "Account verification successful"}, status_code=200)

    def resend_confirmation_code(email: EmailStr, cognito: AWS_Cognito):
        """認証コード再送信

        Args:
            email (EmailStr): メールアドレス
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.check_user_exists(email)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "UserNotFoundException":
                raise HTTPException(
                    status_code=404, detail="User does not exist"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            try:
                response = cognito.resend_confirmation_code(email)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "UserNotFoundException":
                    raise HTTPException(
                        status_code=404, detail="User not found"
                    )
                elif e.response["Error"]["Code"] == "LimitExceededException":
                    raise HTTPException(
                        status_code=429, detail="Limit exceeded"
                    )
                else:
                    raise HTTPException(status_code=500, detail="Internal Server")
            else:
                return JSONResponse(content={"message": "Confirmation code sent successfully"}, status_code=200)

    def user_signin(data: UserSignIn, cognito: AWS_Cognito):
        """ログイン

        Args:
            data (UserSignIn): ログインフォーム
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.user_signin(data)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "UserNotFoundException":
                raise HTTPException(
                    status_code=404, detail="User does not exist"
                )
            elif e.response["Error"]["Code"] == "UserNotConfirmedException":
                raise HTTPException(
                    status_code=403, detail="Please verify your account"
                )
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise HTTPException(
                    status_code=401, detail="Incorrect username or password"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            content = {
                "message": "User signed in successfully",
                "AccessToken": response["AuthenticationResult"]["AccessToken"],
                "RefreshToken": response["AuthenticationResult"]["RefreshToken"]
            }
            return JSONResponse(content=content, status_code=200)

    def forgot_password(email: EmailStr, cognito: AWS_Cognito):
        """パスワード忘れ：再発行申請

        Args:
            email (EmailStr): メールアドレス
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.forgot_password(email)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "UserNotFoundException":
                raise HTTPException(
                    status_code=404, detail="User does not exist"
                )
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                raise HTTPException(
                    status_code=403, detail="Unverified account"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return JSONResponse(content={"message": "Password reset code sent to your email address"}, status_code=200)

    def confirm_forgot_password(data: ConfirmForgotPassword, cognito: AWS_Cognito):
        """パスワード忘れ：パスワード変更

        Args:
            data (ConfirmForgotPassword): パスワード再設定フォーム
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.confirm_forgot_password(data)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredCodeException":
                raise HTTPException(
                    status_code=403, detail="Code expired"
                )
            elif e.response["Error"]["Code"] == "CodeMismatchException":
                raise HTTPException(
                    status_code=400, detail="Code does not match."
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return JSONResponse(content={"message": "Password reset successfully"}, status_code=200)

    def change_password(data: ChangePassword, cognito: AWS_Cognito):
        """パスワード変更

        Args:
            data (ChangePassword): パスワード変更フォーム
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.change_password(data)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidParameterException":
                raise HTTPException(
                    status_code=400, detail="Access token provided has wrong format"
                )
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise HTTPException(
                    status_code=401, detail="Incorrect username or password."
                )
            elif e.response["Error"]["Code"] == "LimitExceededException":
                raise HTTPException(
                    status_code=429, detail="Attempt limit exceeded, please try again later"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return JSONResponse(content={"message": "Password changed successfully"}, status_code=200)

    def new_access_token(refresh_token: str, cognito: AWS_Cognito):
        """アクセストークン再発行

        Args:
            refresh_token (str): トークン
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.new_access_token(refresh_token)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidParameterException":
                raise HTTPException(
                    status_code=400, detail="Refresh token provided has wrong format"
                )
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise HTTPException(
                    status_code=401, detail="Invalid refresh token provided"
                )
            elif e.response["Error"]["Code"] == "LimitExceededException":
                raise HTTPException(
                    status_code=429, detail="Attempt limit exceeded, please try again later"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            content = {
                "message": "Refresh token generated successfully",
                "AccessToken": response["AuthenticationResult"]["AccessToken"],
                "ExpiresIn": response["AuthenticationResult"]["ExpiresIn"],
            }
            return JSONResponse(content=content, status_code=200)

    def logout(access_token: str, cognito: AWS_Cognito):
        """ログアウト

        Args:
            access_token (str): アクセストークン
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            response = cognito.logout(access_token)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidParameterException":
                raise HTTPException(
                    status_code=400, detail="Access token provided has wrong format"
                )
            elif e.response["Error"]["Code"] == "NotAuthorizedException":
                raise HTTPException(
                    status_code=401, detail="Invalid access token provided"
                )
            elif e.response["Error"]["Code"] == "TooManyRequestsException":
                raise HTTPException(
                    status_code=429, detail="Too many requests"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return

    def user_details(email: EmailStr, cognito: AWS_Cognito):
        """ユーザ情報取得

        Args:
            email (EmailStr): メールアドレス
            cognito (AWS_Cognito): AWSCognito
        """
        try:
            logging.info(email)
            response = cognito.check_user_exists(email)
        except botocore.exceptions.ClientError as e:
            logging.info(e)
            if e.response["Error"]["Code"] == "UserNotFoundException":
                raise HTTPException(
                    status_code=404, detail="User does not exist"
                )
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            user = {}
            for attribute in response["UserAttributes"]:
                user[attribute["Name"]] = attribute["Value"]
            return JSONResponse(content=user, status_code=200)
