import json
from typing import Dict

from localTypes import Route, Default_response, RouteError, DefaultResponseError


class Config:
    HOST: str = ""
    PORT: int = 9999
    ROUTES: Route = dict()
    DEFAULT_RESPONSES: Default_response = dict()

    @classmethod
    def init_config(cls, config_file: str) -> None:
        with open(config_file, "r") as file:
            json_content: Dict = json.load(file)
        cls.HOST = json_content.get("host") or ""
        cls.PORT = json_content.get("port") or 9999
        cls.ROUTES = cls._parse_command(json_content.get("routes"))
        cls.DEFAULT_RESPONSES = cls._parse_default_response(json_content.get("default_responses"))

    @staticmethod
    def _parse_command(routes: Route) -> Route:
        for key, value in routes.items():
            value_keys = list(value.keys())
            if "method" not in value_keys:
                routes[key]["method"] = "GET"
            if "params" not in value_keys:
                routes[key]["params"] = []
            if "return_stdout" not in value_keys:
                routes[key]["return_stdout"] = True
            if "commands" not in value_keys or routes[key]["commands"] == []:
                raise RouteError("At least one command is required")

            for index, command_list in enumerate(routes[key]["commands"]):
                key_list = list(command_list.keys())
                if "command" not in key_list or command_list["command"] in ["", None]:
                    raise RouteError("A command is required")
                if "stdin" not in key_list:
                    routes[key]["commands"][index]["stdin"] = None
                if "pipe_to_stdin" not in key_list:
                    routes[key]["commands"][index]["pipe_to_stdin"] = False
                if "expected_return_code" not in key_list:
                    routes[key]["commands"][index]["expected_return_code"] = None
                if "return_stderr_on_error" not in key_list:
                    routes[key]["commands"][index]["return_stderr_on_error"] = True
                routes[key]["commands"][index]["stdout"] = None
        return routes

    @staticmethod
    def _parse_default_response(responses: Default_response) -> Default_response:
        for key, value in responses.items():
            try:
                int(key)
            except ValueError:
                raise DefaultResponseError("Key must be a int response code")
            value_keys = value.keys()
            if value["type"] not in ["string", "file"]:
                raise DefaultResponseError("Unknown response type")
            if value["type"] == "string":
                if "text" not in value_keys:
                    raise DefaultResponseError("'text' field required when using type string")
            if value["type"] == "file":
                if "location" not in value_keys:
                    raise DefaultResponseError("'location' field required when using type file")
                if "mime_type" not in value_keys:
                    raise DefaultResponseError("'mime_type' field required when using type file")
        return responses
