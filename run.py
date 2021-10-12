#  https://basicdashflask.herokuapp.com/
import flask
from dashboard.dash1 import create_dash1_application

server = flask.Flask(__name__)

create_dash1_application(server)

@server.route('/')
def hello():
    return flask.redirect('dash1')


if __name__ == '__main__':
   server.run()
