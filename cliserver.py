import io
import argparse

from commander import Commander
from config_parser import Config
from wsgiref.simple_server import make_server
from typing import Dict, Any, Iterable, Union, List, Tuple, Callable

from inspector import inspector
from local_types import ResponseEnum
from responder import Responder
from params import merge_request_params

# Try to import wsgiref.types or define the type custom if the import fails
try:
    from wsgiref.types import StartResponse
except ImportError:
    StartResponse = Callable[[str, List[Tuple[str, str]]], None]

parser = argparse.ArgumentParser(prog="CliServer", description="Turn the command line into an API")
parser.add_argument("filename")
args = parser.parse_args()

c = Config()
c.init_config(args.filename)

responder = Responder(c.DEFAULT_RESPONSES)


def app(environ: Dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
    path: str = environ.get("PATH_INFO")
    method: str = environ.get("REQUEST_METHOD")
    query: str = environ.get("QUERY_STRING")
    content_type: str = environ.get("CONTENT_TYPE")
    content_length: Union[str, int] = environ.get("CONTENT_LENGTH") or 0
    body: io.BufferedReader = environ.get("wsgi.input")

    route = c.ROUTES.get(path)
    if not route:
        return responder.respond(start_response, ResponseEnum.NotFound, None, None)
    if route["method"] != method:
        return responder.respond(start_response, ResponseEnum.MethodNotAllowed, None, [("allow", route.get("method"))])
    if len(route["params"]) > 0:
        param_dict = merge_request_params(query, content_type, content_length, body)
        status, value = inspector(param_dict)
        if status != ResponseEnum.OK:
            return responder.respond(start_response, ResponseEnum.BadRequest, value, None)
    else:
        param_dict = dict()
    commander = Commander(route["commands"], route["return_stdout"], len(route["params"]) > 0, param_dict)
    status, value = commander.execute_commands()
    return responder.respond(start_response, status, value, None)


if __name__ == "__main__":
    with make_server(c.HOST, c.PORT, app) as server:
        server.serve_forever()
