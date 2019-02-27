from flask import Flask, request
from flask import jsonify
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import uuid
import os
import subprocess
import time

#Tokens need to be refreshed every X amount of hour
#So you need to run this script again..
relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

output = subprocess.check_output(['curl', url])

data = json.loads(output)

os.environ["AWS_ACCESS_KEY_ID"] = data['AccessKeyId']
os.environ["AWS_SECRET_ACCESS_KEY"] = data['SecretAccessKey']
os.environ["AWS_SESSION_TOKEN"] = data['Token']

app = Flask(__name__)

host = "a29zo009haxq0r-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
sub_topic = "WebInterface/iot/sub"
port = 443

data = {}

myAWSIoTMQTTClient = AWSIoTMQTTClient(str(uuid.uuid4()), useWebsocket=True)
myAWSIoTMQTTClient.configureEndpoint(host,port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(25)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
myAWSIoTMQTTClient.connect()

def Callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    data['Message'] = message
    Callback.has_been_called = True

myAWSIoTMQTTClient.subscribe(sub_topic, 0, Callback)

#Route
@app.route('/device/<DeviceId>', methods=['GET', 'POST'])
def PublishToIoT(DeviceId):

    pub_topic = "Webinterface/iot/pub/" + DeviceId

    global data

    if request.method == 'GET':
         data = {"status": "GET"}

    data = jsonify(data)
    
    message = {}
    message['DeviceId'] = DeviceId
    message = json.dumps(message)

    myAWSIoTMQTTClient.publish(pub_topic, message,0)

    while not Callback.has_been_called:
        time.sleep(0.1)

    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
