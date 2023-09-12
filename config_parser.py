import json
from typing import Dict, List

from local_types import Route, Default_response, RouteError, DefaultResponseError, RouteBody, CommandBody, ParsedRoute


class Config:
    HOST: str = ""
    PORT: int = 9999
    ROUTES: ParsedRoute = dict()
    DEFAULT_RESPONSES: Default_response = dict()

    @classmethod
    def init_config(cls, config_file: str) -> None:
        with open(config_file, "r") as file:
            json_content: Dict = json.load(file)
        cls.HOST = json_content.get("host") or ""
        cls.PORT = json_content.get("port") or 9999
        cls.ROUTES = cls._parse_routes(json_content.get("routes"))
        cls.DEFAULT_RESPONSES = cls._parse_default_response(json_content.get("default_responses"))

    @staticmethod
    def _set_default_route_values(route: RouteBody) -> RouteBody:
        keys = list(route.keys())
        if "method" not in keys:
            route["method"] = "GET"
        if "params" not in keys:
            route["params"] = []
        if "return_stdout" not in keys:
            route["return_stdout"] = True
        if "variables" not in keys:
            route["variables"] = {}
        return route

    @staticmethod
    def _enforce_mandatory_route_values(route: RouteBody) -> RouteBody:
        keys = list(route.keys())
        if "commands" not in keys or route["commands"] == []:
            raise RouteError("At least one command is required")
        return route

    @staticmethod
    def _set_default_command_values(command: CommandBody) -> CommandBody:
        keys = list(command.keys())
        if "stdin" not in keys:
            command["stdin"] = None
        if "pipe_to_stdin" not in keys:
            command["pipe_to_stdin"] = False
        if "expected_return_code" not in keys:
            command["expected_return_code"] = None
        if "return_stderr_on_error" not in keys:
            command["return_stderr_on_error"] = True
        if "condition" not in keys:
            command["condition"] = None
        command["stdout"] = None
        return command

    @staticmethod
    def _enforce_mandatory_command_values(command: CommandBody) -> CommandBody:
        keys = list(command.keys())
        if "command" not in keys or command["command"] in ["", None]:
            raise RouteError("A command is required")
        return command

    @classmethod
    def _parse_routes(cls, routes: Route) -> ParsedRoute:
        if routes is None:
            return dict()
        return_routes: ParsedRoute = {}
        for key, value in routes.items():
            value = cls._enforce_mandatory_route_values(value)
            value = cls._set_default_route_values(value)

            return_commands: List[CommandBody] = []
            for index, command in enumerate(routes[key]["commands"]):
                command = cls._enforce_mandatory_command_values(command)
                command = cls._set_default_command_values(command)
                return_commands.append(command)
            value["commands"] = return_commands
            return_routes[key] = value
        return return_routes

    @staticmethod
    def _parse_default_response(responses: Default_response) -> Default_response:
        if responses is None:
            return dict()
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
