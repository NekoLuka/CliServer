from typing import Dict, Tuple

from local_types import ResponseEnum


def inspector(params: Dict[str, str]) -> Tuple[ResponseEnum, str]:
    error_string = "{symbol} is not allowed in commands or conditions"
    for value in params.values():
        if "&&" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol="&&")
        elif "||" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol="||")
        elif ">" in value:
            return ResponseEnum.BadRequest, error_string.format(symbol=">")
    return ResponseEnum.OK, ""
