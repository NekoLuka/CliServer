import json
from typing import Dict

from types import Route, Default_response


class Config:
    HOST: str = ""
    PORT: int = 9999

    # Example:
    # "routes": {
    #     "/hello": {
    #         "method": "GET",
    #         "params": ["message"],
    #         "commands": [
    #           {
    #               "command": "echo {message}",
    #               "stdin": null,
    #               "pipe_to_stdin": true,
    #               "expected_return_code": 0,
    #               "return_stderr_on_error": true
    #           },
    #           {
    #               "command": "base64",
    #               "stdin": null,
    #               "pipe_to_stdin": false,
    #               "expected_return_code": 0,
    #               "return_stdout": true
    #           }
    #         ]
    #     }
    # }
    ROUTES: Route = dict()

    # Example:
    # "default_responses": {
    #     "404": {
    #         "type": "string",
    #         "text": "This path was not found"
    #     },
    #     "500": {
    #         "type": "file",
    #         "location": "500.txt",
    #         "mime_type": "text/plain"
    #     }
    # }
    DEFAULT_RESPONSES: Default_response = dict()

    @classmethod
    def init_config(cls, config_file: str) -> None:
        with open(config_file, "r") as file:
            json_content: Dict = json.load(file)
        cls.HOST = json_content.get("host") or ""
        cls.PORT = json_content.get("port") or 9999


    @staticmethod
    def _parse_command(routes: Route) -> Route:
        pass
