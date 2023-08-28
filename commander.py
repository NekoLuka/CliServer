import subprocess
from typing import Dict, Union, List, Tuple

from local_types import CommandBody, MissingParameterError, ResponseEnum


class Commander:
    def __init__(self, commands: List[CommandBody], return_stdout: bool = True,
                 use_params: bool = True, params: Dict[str, str] = None):
        self.commands = commands
        self.return_stdout = return_stdout
        self.params = params
        self.use_params = use_params
        self.command_stack: List[CommandBody] = []

    def get_correct_stdin(self, stdin_param: Union[str, None]) -> Union[str, None]:
        if self.use_params and stdin_param:
            return self.params.get(stdin_param)
        if len(self.command_stack) > 0 and self.command_stack[-1]["pipe_to_stdin"]:
            return self.command_stack[-1]["stdout"]

    def format_command(self, command: str) -> str:
        if self.use_params:
            try:
                return command.format(**self.params)
            except KeyError as e:
                raise MissingParameterError(f"{str(e)} was expected but not found")
        return command

    @staticmethod
    def check_return_code(return_code: int, expected_return_code: int):
        return return_code != expected_return_code

    def execute_commands(self) -> Tuple[ResponseEnum, Union[str, None]]:
        for command in self.commands:
            try:
                cmd = self.format_command(command["command"])
            except MissingParameterError as e:
                return ResponseEnum.BadRequest, str(e)
            p = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            stdout, stderr = p.communicate(self.get_correct_stdin(command["stdin"]))
            if type(command["expected_return_code"]) is int \
                    and not self.check_return_code(p.returncode, command["expected_return_code"]):
                return ResponseEnum.InternalServerError, stderr if command["return_stderr_on_error"] else None
            command["stdout"] = stdout
            self.command_stack.append(command)
        if self.return_stdout:
            return ResponseEnum.OK, self.command_stack[-1]["stdout"]
        return ResponseEnum.NoContent, None
