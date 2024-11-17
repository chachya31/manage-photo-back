from typing import List

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    loc: List[str] = Field(..., description="エラー箇所")
    msg: str = Field(..., description="エラーメッセージ")
    type: str = Field(..., description="エラータイプ")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "loc": [],
                "msg": "1文字以上であるひつようがあります",
                "type": "value_error"
            }
        }


class ErrorJsonResponse(BaseModel):
    detail: List[ErrorDetail] = Field(..., description="エラーメッセージ")
