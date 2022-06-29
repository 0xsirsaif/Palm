"""
TODO / hypothesis / notes / anger ..etc:
    - the route method don't do the actually work like the normal decorator, instead it updates the `routes`. handle the
    request inside this decorator
    - too many static functions
    - once the server is run, the decorated functions in the app.py run and inside the `routes` it assigns every route
    to its function (handler)
    -
"""

import functools
import inspect

from webob import Request, Response
import parse


class Palm:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response, *args, **kwargs):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def find_the_handler(self, request_path):
        for path, handler in self.routes.items():
            parsed_path = parse.parse(path, request_path)
            if parsed_path:
                return handler, parsed_path.named

        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_the_handler(request.path)
        if handler:
            if inspect.isclass(handler):
                method = getattr(handler(), request.method.lower(), None)
                if not method:
                    raise AttributeError(f"Method {method} is not allowed")
                method(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            self.not_found_response(response)

        return response

    def route(self, path):
        """
        Get the proper handler for the path.
        """

        def wrapper(handler):
            print(f"Got {path}. Add to routes")
            self.routes[path] = handler
            return handler

        assert path not in self.routes, f"route {path} already exists"

        return wrapper

    def not_found_response(self, response):
        response.status = "404"
        response.text = "Not Found, nigga!"
