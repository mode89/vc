import flask

class Server(flask.Flask):

    def __init__(self, name):
        flask.Flask.__init__(self, name)
        self.add_url_rule("/",
            methods=["GET", "POST"], view_func=self.index)

    def run(self):
        flask.Flask.run(self, host="0.0.0.0")

    def index(self):
        return flask.render_template("index.html")
