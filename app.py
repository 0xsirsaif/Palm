import datetime

from api import API


app = API()


# home = route(home)
# home("/path")
# TODO: Question.
#   1. his implementation is route(path) -> wrapper(func) vs mine is route(func) -> wrapper(path) ?
#   answer: decorator with an arguments have a bit different implementation. [decorator factory]
#   decorator with argument translated to this:
#       home = route(path)(home) instead of the above version
@app.route("/home")
def home(request, response):
    response.text = "home page"


@app.route("/about")
def about(request, response):
    response.text = "about page"


@app.route("/hello/{name}")
def helo(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/age/{birthdate:tg}")
def calculate_age(request, response, birthdate):
    age = datetime.datetime.utcnow() - birthdate
    response.text = f"Age is: {age}"
