from flask import Flask
from threading import Thread

import requestHandler
import responseHandler

requestApp = Flask(__name__)
requestApp.register_blueprint(requestHandler.requestView)

responseApp = Flask(__name__)
requestApp.register_blueprint(responseHandler.responseView)

def runRequestApp():
    requestApp.run(host='0.0.0.0', port=80)

def runResponseApp():
    responseApp.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t1 = Thread(target=runRequestApp())
    t2 = Thread(target=runResponseApp())
    t1.start()
    t2.start()