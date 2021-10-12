#  https://basicdashflask.herokuapp.com/
from flask import *
from dashboard.dash1 import create_dash1_application

server = Flask(__name__)

create_dash1_application(server)

@server.route('/',methods=['GET'])
def hello():
    return redirect('dash1')


if __name__ == '__main__':
   server.run()
