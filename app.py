from flask import Flask, request
from flask import jsonify
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import uuid

app = Flask(__name__)

host = "a29zo009haxq0r-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
port = 443

myAWSIoTMQTTClient = AWSIoTMQTTClient(str(uuid.uuid4()), useWebsocket=True)

myAWSIoTMQTTClient.configureEndpoint(host,port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath) 

myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(25)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

myAWSIoTMQTTClient.connect()

#Route
@app.route('/handle', methods=['GET', 'POST'])
def login():

    data = {"status":"We good fam :)"}
    data = jsonify(data)
    # if request.method == 'POST':
    #      data = {"status": "POST"}
    # else:
    #      data = {"status": "GET"}
    # return jsonify(data)

    myAWSIoTMQTTClient.publish("weird/topic", data,0)
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
