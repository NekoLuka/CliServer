from localTypes import Default_response
from wsgiref.types import StartResponse
from typing import Dict, Any, Iterable, Union, Tuple, List


class DefaultResponse:
    def __init__(self, config: Default_response):
        self.config = config

    def call_error(self,
                   error_code: str,
                   start_response: StartResponse,
                   headers: List[Tuple[str, str]] = None) -> Iterable[bytes]:
        body = b""
        if code_config := self.config.get(error_code[:3]):
            if code_config["type"] == "string":
                body = code_config.get("text").encode()
            elif code_config["type"] == "file":
                pass

        start_response(error_code, headers or [])
        return [body]


