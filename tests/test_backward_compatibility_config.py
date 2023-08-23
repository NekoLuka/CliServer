from configparser import Config


def test_backwards_compatibility_routes():
    config = {"/hello": {"commands": [{"command": "echo hello world"}]}}
    response = Config()._parse_command(config)
    route_body = response.get("/hello")

    assert route_body is not None, "No route body found in output"
    assert type(route_body["method"]) is str, "method should be str"
    assert type(route_body["params"]) is list, "params should be a list"
    assert type(route_body["return_stdout"]) is bool, "return_stdout should be a bool"
    assert type(route_body["commands"]) is list, "commands should be a list"

    command_body = route_body["commands"][0]

    assert command_body is not None, "Command body should not be empty"
    assert type(command_body["command"]) is str, "command should be str"
    assert type(command_body["stdin"]) is str or command_body["stdin"] is None, "stdin should be a str"
    assert type(command_body["pipe_to_stdin"]) is bool, "pipe_to_stdin should be str"
    assert type(command_body["expected_return_code"]) is int, "expected_return_code should be int"
    assert type(command_body["return_stderr_on_error"]) is bool, "return_stderr_on_error should be bool"
