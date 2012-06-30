from thirdplace.core import app


@app.route('/')
def hello():
    return "Hello, world!"
