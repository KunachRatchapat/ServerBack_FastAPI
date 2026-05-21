from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    code: str = "200"
    status: str = "success"
    message: str = "OK"
    result: Optional[T] = None


def success_response(data: Optional[T] = None, message: str = "OK") -> ResponseSchema[T]:
    return ResponseSchema(code="200", status="success", message=message, result=data)


def created_response(data: Optional[T] = None, message: str = "Created") -> ResponseSchema[T]:
    return ResponseSchema(code="201", status="success", message=message, result=data)
