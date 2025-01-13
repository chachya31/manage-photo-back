import requests
from fastapi import Depends, HTTPException

from .config import env_vars
from .JWTBearer import JWKS, JWTBearer, JWTAuthorizationCredentials


AWS_REGION_NAME = env_vars.AWS_REGION_NAME
AWS_COGNITO_APP_CLIENT_ID = env_vars.AWS_COGNITO_APP_CLIENT_ID
AWS_COGNITO_USER_POOL_ID = env_vars.AWS_COGNITO_USER_POOL_ID

jwks = JWKS.model_validate(
    requests.get(
        f"https://cognito-idp.{AWS_REGION_NAME}.amazonaws.com/{AWS_COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    ).json()
)

auth = JWTBearer(jwks)

async def get_current_user(
    credentials: JWTAuthorizationCredentials = Depends(auth)
) -> str:
    try:
        return credentials.claims["username"]
    except KeyError:
        HTTPException(status_code=403, detail="Username missing")
    except Exception as e:
        print(e)
