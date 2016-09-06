import flask
import unittest

class TaggerTests(unittest.TestCase):

    def test_hello_world(self):
        app = flask.Flask(__name__)
        @app.route("/")
        def hello_world():
            return "Hello, World!"
        app.run(host="0.0.0.0")

    def test_render_template(self):
        app = flask.Flask(__name__)
        @app.route("/")
        def hello():
            return flask.render_template("hello.html")
        app.run(host="0.0.0.0")

    def test_button(self):
        app = flask.Flask(__name__)
        @app.route("/")
        def hello():
            return flask.render_template("button.html")
        @app.route("/button", methods=["POST"])
        def button():
            print("Pressed button")
            return flask.redirect("/")
        app.run(host="0.0.0.0")

if __name__ == "__main__":
    unittest.main()
