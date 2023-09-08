from typing import Union, List, Tuple

from local_types import ParsedRoute, ResponseEnum, ParsedRouteBody


class Router:
    def __init__(self, config: ParsedRoute):
        self.config = config

    def route(self, path: str, method: str) -> Tuple[ResponseEnum, Union[List[Tuple[str, str]], None, ParsedRouteBody]]:
        route = self.config.get(path)
        if not route:
            return ResponseEnum.NotFound, None
        if route["method"] != method:
            return ResponseEnum.MethodNotAllowed, [("allow", route["method"])]
        return ResponseEnum.OK, route
