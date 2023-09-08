from enum import Enum
from typing import Dict, Union, List, Literal, TypedDict


class CommandBody(TypedDict):
    command: str
    stdin: Union[None, str]
    pipe_to_stdin: Union[None, bool]
    expected_return_code: Union[None, int]
    return_stderr_on_error: bool
    condition: Union[None, str]
    stdout: Union[None, str]


class RouteBody(TypedDict):
    method: str
    params: Union[None, List[str]]
    return_stdout: bool
    commands: List[CommandBody]


class ParsedRouteBody(TypedDict):
    method: str
    params: Union[None, List[str]]
    return_stdout: bool
    commands: List[CommandBody]


Route = Dict[str, RouteBody]
ParsedRoute = Dict[str, ParsedRouteBody]


class DefaultResponseBody(TypedDict):
    type: Literal["string", "file"]
    text: str
    location: str
    mime_type: str


Default_response = Dict[str, DefaultResponseBody]


class RouteError(Exception):
    pass


class DefaultResponseError(Exception):
    pass


class MissingParameterError(Exception):
    pass


class ResponseEnum(Enum):
    NoContent = 1
    BadRequest = 2
    InternalServerError = 3
    OK = 4
    NotFound = 5
    MethodNotAllowed = 6
