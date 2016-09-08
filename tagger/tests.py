import flask
import server
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
                        <input type="submit"
                            name="button"
                            value="Button"/>
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
                <style>
                    .buttons {
                        position: fixed;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                    }

                    .button input {
                        width: 500px;
                        height: 100px;
                        border-radius: 25px;
                        font-size: 50px;
                        margin: 10px;
                    }
                </style>
                <body>
                    <form action="/" method="post">
                        <div class="buttons">
                            <table>
                                <tr>
                                    <div class="button">
                                        <input type="submit"
                                            name="button1"
                                            value="Button1"/>
                                    </div>
                                </tr>
                                <tr>
                                    <div class="button">
                                        <input type="submit"
                                            name="button2"
                                            value="Button2"/>
                                    </div>
                                </tr>
                            </table>
                        </div>
                    </form>
                </body>
            """)
        app.run(host="0.0.0.0")

    def test_server(self):
        srv = server.Server(__name__)
        srv.run()

if __name__ == "__main__":
    unittest.main()
