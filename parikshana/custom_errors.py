from rest_framework.response import Response
from typing import Union, Optional
from rest_framework.exceptions import APIException


class BaseExceptions(APIException):
    message = ""
    data = {}
    status_code = 0

    def __init__(
        self,
        message: Optional[str] = None,
        data: Optional[Union[list, dict]] = None,
        status_code: Optional[int] = None,
    ):
        """Init Function to initialise the problem"""
        if message:
            self.message = message
        if data:
            self.data = data
        if status_code:
            self.status_code = status_code


class Http400(BaseException):
    message = "Something went wrong on your side."
    status_code = 400


class Http401(BaseException):
    message = "Begone Wench! Thou shant haveth the authorization"
    status_code = 401


class Http402(BaseException):
    message = "Paisa feko nahi toh chalte bano miya!"
    status_code = 402


class Http403(BaseException):
    message = "You dont have access to view this!"
    status_code = 403


class Http404(BaseExceptions):
    message = "The data you are looking for is not found!"
    status_code = 404


class Http418(BaseException):
    message = "Mereko kya main toh teapot hu"
    status_code = 418


class Http500(BaseException):
    message = "Something went wrong internally. Please contact the administrator"
    status_code = 500


class Http200(BaseException):
    message = "OK"
    status_code = 200


class Http201(BaseException):
    message = "Object is created Successfully!"


validExceptions = (
    Http400,
    Http401,
    Http402,
    Http403,
    Http404,
    Http418,
    Http500,
    Http200,
    Http201,
)


class ExceptionMixin:
    def handle_exception(self, exc):
        """A low profile exception Handler base"""
        if exc in validExceptions:
            return Response(
                data={
                    "message": exc.message,
                    "data": exc.data,
                },
                status=exc.status_code,
            )
        "Pass through error if unhandled"
        return super().handle_exception(exc)
