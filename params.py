import io
import json
import urllib.parse
from typing import Union, Dict


def merge_request_params(query: str, content_type: str, content_length: Union[str, int], body: io.BufferedReader) -> \
        Dict[str, str]:
    query_params = {key: " ".join(value) for key, value in urllib.parse.parse_qs(query).items()}
    if content_type == "application/json" and type(content_length) is int and content_length > 0:
        return {**query_params, **json.load(body)}
    else:
        return query_params
