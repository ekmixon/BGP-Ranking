#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, MutableMapping


class ReverseProxied():
    def __init__(self, app: Any) -> None:
        self.app = app

    def __call__(self, environ: MutableMapping[str, Any], start_response: Any) -> Any:
        if scheme := environ.get('HTTP_X_FORWARDED_PROTO') or environ.get(
            'HTTP_X_SCHEME'
        ):
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
