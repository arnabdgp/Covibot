import flask
from dashboard.dash1 import create_dash1_application
from dashboard.dash2 import create_dash2_application

server = flask.Flask(__name__)

create_dash1_application(server)
create_dash2_application(server)

@server.route('/')
@server.route('/hello')
def hello():
    return flask.redirect('dash1')


if __name__ == '__main__':
   server.run()
