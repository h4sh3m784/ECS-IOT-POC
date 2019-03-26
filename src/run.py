from flask import Flask
from threading import Thread
from requestHandler import requestView
from responseHandler import responseView

requestApp = Flask(__name__)
requestApp.register_blueprint(requestView)

responseApp = Flask(__name__)
requestApp.request_blueprint(responseView)

def runRequestApp():
    requestApp.run(host='0.0.0.0', port=80)

def runResponseApp():
    responseApp.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t1 = Thread(target=runRequestApp())
    t2 = Thread(target=runResponseApp())
    t1.start()
    t2.start()