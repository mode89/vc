import flask
import unittest

class TestTagger(unittest.TestCase):

    def test_flask_hello_world(self):
        app = flask.Flask(__name__)
        @app.route("/")
        def hello_world():
            return "Hello, World!"
        app.run(host="0.0.0.0")

if __name__ == "__main__":
    unittest.main()
