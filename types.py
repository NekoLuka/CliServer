from typing import Dict, Union, List, Literal

Route = Dict[str, Dict[
        Literal["method", "params", "commands"], Union[
            str, List[str], List[Dict[
                Literal["command",
                "stdin",
                "pipe_to_stdin",
                "expected_return_code",
                "return_stderr_on_error",
                "return_stdout"], Union[str, bool, int, None]
            ]
            ]]
    ]]
Default_response = Dict[str, Dict[Literal["type", "text", "location", "mime_type"], str]]
