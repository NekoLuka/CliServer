from typing import Callable, List, Tuple

from local_types import ResponseEnum, Default_response

try:
    from wsgiref.types import StartResponse
except ImportError:
    StartResponse = Callable[[str, List[Tuple[str, str]]], None]


class Responder:
    def __init__(self, config: Default_response):
        self.config = config

    def respond(self,
                start_response: StartResponse,
                status: ResponseEnum,
                value: str = None,
                headers: List[Tuple[str, str]] = None
                ) -> List[bytes]:
        match status:
            case ResponseEnum.NoContent:
                status_message = "204 no content"
            case ResponseEnum.BadRequest:
                status_message = "400 bad request"
            case ResponseEnum.NotFound:
                status_message = "404 not found"
            case ResponseEnum.MethodNotAllowed:
                status_message = "405 method not allowed"
            case ResponseEnum.InternalServerError:
                status_message = "500 internal serer error"
            case _:
                status_message = "200 ok"
        start_response(status_message, headers or [])
        if code_config := self.config.get(status_message[:3]):
            if code_config["type"] == "string":
                return code_config.get("text").encode()
        return [value.encode()] if value else []
