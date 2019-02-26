from flask import Flask, request
from flask import jsonify
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import uuid
import os
import socket
import subprocess

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

print(relative_URI)

print(url)

output = subprocess.check_output(['curl', url])

print(output)

data = json.loads(output)

os.environ["AWS_ACCESS_KEY_ID"] = data['AccessKeyId']
print(data['AccessKeyId'])
os.environ["AWS_SECRET_ACCESS_KEY"] = data['SecretAccessKey']
print(data['SecretAccessKey'])
os.environ["AWS_SESSION_TOKEN"] = data['Token']
print(data['Token'])

app = Flask(__name__)

#Route
@app.route('/device/<DeviceId>', methods=['GET', 'POST'])
def PublishToIoT(DeviceId):

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
    
    data = {}
    if request.method == 'GET':
         data = {"status": "GET"}
    data = jsonify(data)
    message = {}
    message['DeviceId'] = DeviceId
    message = json.dumps(message)
    myAWSIoTMQTTClient.publish("weird/topic", message,0)
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
