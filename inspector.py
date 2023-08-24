from typing import Dict

from localtypes import ResponseEnum


def inspector(params: Dict[str, str]):
    error_string = "{symbol} is not allowed in commands"
    for value in params.values():
        if "&&" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol="&&")
        elif "||" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol="||")
        elif ">" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol=">")
    return ResponseEnum.OK, ""
