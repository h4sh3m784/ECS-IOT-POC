from flask import Flask
from flask import request
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import uuid
import os
import subprocess
import time
import socket

import logging
import os
import threading
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
port = 443

response = dict()

myAWSIoTMQTTClient = AWSIoTMQTTClient(str(uuid.uuid4()), useWebsocket=True)
myAWSIoTMQTTClient.configureEndpoint(host,port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(25)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
myAWSIoTMQTTClient.connect()

counter = 1

myDict = {}
myEventDict = {}

@app.route('/request-device/<device_id>', methods=['POST'])
def request_device(device_id):

    logger.debug("Request to publish to " + device_id)

    pub_topic = "api/iot/pub/" + device_id

    request_body = json.loads(request.data)

    global counter  
    thisRequestId = str(counter)
    counter = counter + 1
    pub_message = dict()
    pub_message['DeviceId'] = device_id
    pub_message['Message'] = request_body['Message']
    pub_message['EndPoint'] = socket.gethostname() + "/response-device/" + device_id
    pub_message['RequestId'] = thisRequestId
    pub_message = json.dumps(pub_message)

    logger.debug("Publishing message: " + json.dumps(pub_message))

    myAWSIoTMQTTClient.publish(pub_topic, pub_message, 0)

    time_out = False

    logger.debug("Waiting for " + thisRequestId)

    waitCounter = 0

    event = threading.Event()
    myEventDict[thisRequestId] = event
    event.wait(10)

    logger.debug("Received the response..")
    response = myDict[thisRequestId]

    response = json.dumps(response)

    return response

@app.route('/response-device/<device_id>', methods=['POST'])
def response_device(device_id):

    response = json.loads(request.data)
    logger.debug(response)
    myDict[response['RequestId']] = response
    myEventDict[response['RequestId']].set()
    
    return json.loads('{"Status: "200"')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
