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
            return flask.render_template_string("""
                <!doctype html>
                <title>Tagger</title>
                <body>Hello, World!</body>
            """)
        app.run(host="0.0.0.0")

    def test_button(self):
        app = flask.Flask(__name__)
        @app.route("/")
        def hello():
            return flask.render_template_string("""
                <!doctype html>
                <title>Tagger</title>
                <body>
                    <form action="/button" method="post">
                        <input type="submit" name="button" value="Button"/>
                    </form>
                </body>
            """)
        @app.route("/button", methods=["POST"])
        def button():
            print("Pressed button")
            return flask.redirect("/")
        app.run(host="0.0.0.0")

    def test_buttons(self):
        app = flask.Flask(__name__)
        @app.route("/", methods=["GET", "POST"])
        def form():
            if "button1" in flask.request.form:
                print("Pressed the first button")
            elif "button2" in flask.request.form:
                print("Pressed the second button")
            return flask.render_template_string("""
                <!doctype html>
                <title>Tagger</title>
                <body>
                    <form action="/" method="post">
                        <input type="submit"
                            name="button1" value="Button1"/>
                        <input type="submit"
                            name="button2" value="Button2"/>
                    </form>
                </body>
            """)
        app.run(host="0.0.0.0")

if __name__ == "__main__":
    unittest.main()
