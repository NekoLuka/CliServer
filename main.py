import io
import subprocess

from configParser import Config
from wsgiref.simple_server import make_server
from wsgiref.types import StartResponse
from typing import Dict, Any, Iterable, Union, List
from defaultResponse import DefaultResponse
from localTypes import CommandBody

c = Config()
c.init_config("default_config.json")

defaultResponse = DefaultResponse(c.DEFAULT_RESPONSES)


def execute_commands(commands: List[CommandBody], use_params: bool = False, params: Dict[str, str] = None) -> (bool, Union[str, None]):
    stdin = None
    for i in commands:
        stdin = i["stdin"]
        p = subprocess.Popen(i["command"].format(**params) if use_params else i["command"])



def app(environ: Dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
    path: str = environ.get("PATH_INFO")
    method: str = environ.get("REQUEST_METHOD")
    query: str = environ.get("QUERY_STRING")
    content_type: str = environ.get("CONTENT_TYPE")
    content_length: Union[str, int] = environ.get("CONTENT_LENGTH") or 0
    body: io.BufferedReader = environ.get("wsgi.input")

    route = c.ROUTES.get(path)
    if not route:
        return defaultResponse.call_error("404 not found", start_response)
    if route.get("method") != method:
        return defaultResponse.call_error("405 method not allowed", start_response, [("allow", route.get("method"))])
    if len(route["params"]) > 0:
        pass  # TODO: parse query string and body to find params
    r = subprocess.Popen("echo hello", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        if r.poll() is not None:
            break
    print(r.returncode)
    print(r.stdout.read())


with make_server(c.HOST, c.PORT, app) as server:
    server.serve_forever()
