from wsgiref.simple_server import make_server


class ReverseEnvs:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(environ, start_response)
        return [data[::-1] for data in wrapped_app_response]


def application(environ, start_response):
    response_body = "\n".join([f"{key}: {value}" for key, value in environ.items()])
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [response_body.encode("utf-8")]


server = make_server("localhost", 5458, app=application)
server.serve_forever()