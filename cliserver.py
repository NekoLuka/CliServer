import io
import json
import subprocess
import urllib.parse
import argparse

from commander import Commander
from configParser import Config
from wsgiref.simple_server import make_server
from typing import Dict, Any, Iterable, Union, List, Tuple, Callable
from localTypes import CommandBody, ResponseEnum
from responder import Responder

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


def execute_commands(
        commands: List[CommandBody],
        use_params: bool = False,
        params: Dict[str, str] = None,
        return_stdout: bool = True
) -> Tuple[int, Union[str, None]]:
    stdin = None
    stdout = None
    for i in commands:
        # Check if all required parameters are present
        if use_params:
            try:
                command = i["command"].format(**params)
            except KeyError as e:
                return 400, f"{str(e)} was expected but not found"
        else:
            command = i["command"]

        # Prepare command
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )
        # Execute command and grab the correct stdin var
        l_stdout, stderr = p.communicate(params.get(i["stdin"]) if use_params and i["stdin"] is not None else stdin)
        # Check if the return code matches the expected one and if not, return an error
        if p.returncode != i["expected_return_code"]:
            if i["return_stderr_on_error"]:
                return 500, stderr
            return 500, None
        # Check if stdout from this command needs to be piped to the next one
        if i["pipe_to_stdin"]:
            stdin = l_stdout
        else:
            stdin = None
        stdout = l_stdout
    # Return the successful results
    if return_stdout:
        return 200, stdout
    return 204, None


def app(environ: Dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
    path: str = environ.get("PATH_INFO")
    method: str = environ.get("REQUEST_METHOD")
    query: str = environ.get("QUERY_STRING")
    content_type: str = environ.get("CONTENT_TYPE")
    content_length: Union[str, int] = environ.get("CONTENT_LENGTH") or 0
    body: io.BufferedReader = environ.get("wsgi.input")

    param_dict: Dict[str, str] = dict()

    route = c.ROUTES.get(path)
    if not route:
        return responder.respond(start_response, ResponseEnum.NotFound, None, None)
    if route["method"] != method:
        return responder.respond(start_response, ResponseEnum.MethodNotAllowed, None, [("allow", route.get("method"))])
    if len(route["params"]) > 0:
        param_dict = {key: " ".join(value) for key, value in urllib.parse.parse_qs(query).items()}
        if content_type == "application/json" and content_length > 0:
            param_dict = {**param_dict, **json.load(body)}
    commander = Commander(route["commands"], route["return_stdout"], len(route["params"]) > 0, param_dict)
    status, value = commander.execute_commands()
    return responder.respond(start_response, status, value, None)


if __name__ == "__main__":
    with make_server(c.HOST, c.PORT, app) as server:
        server.serve_forever()
