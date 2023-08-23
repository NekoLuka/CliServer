import io
import json
import urllib.parse
from typing import Union, Dict


def merge_request_params(query: str, content_type: str, content_length: Union[str, int], body: io.BufferedReader) -> \
        Dict[str, str]:
    query_params = {key: " ".join(value) for key, value in urllib.parse.parse_qs(query).items()}
    try:
        content_length_int = int(content_length)
    except ValueError:
        content_length_int = 0
    if content_type == "application/json" and content_length_int > 0:
        return {**query_params, **json.loads(body.read(content_length_int))}
    else:
        return query_params
