from flask import Flask
from flask import request

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import uuid
import subprocess
import requests
import logging
import os
import threading
import sys

#test change
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()

#Get and Set Credentials for the docker container.
relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

output = subprocess.check_output(['curl', url])

data = json.loads(output)

os.environ["AWS_ACCESS_KEY_ID"] = data['AccessKeyId']
os.environ["AWS_SECRET_ACCESS_KEY"] = data['SecretAccessKey']
os.environ["AWS_SESSION_TOKEN"] = data['Token']

app = Flask(__name__)

#Config
# xray_recorder.configure(
#     service='Demo-APP',
#     sampling_rules=False
# )

# XRayMiddleware(app, xray_recorder)

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


#Dictionaries..
response_Dict = dict()
event_Dict = dict()

endpoint_url = requests.get('http://ip.42.pl/raw').text + "/lambda-response/"

@app.route('/device/<device_id>', methods=['POST'])
def request_device(device_id):

    #logger.debug("Request to publish to " + device_id)

    pub_topic = "api/iot/pub/" + device_id

    request_body = json.loads(request.data)

    thisRequestId = str(uuid.uuid4()) #Create new Request ID

    info ={
        "EndPoint": endpoint_url + device_id,
        "RequestId": thisRequestId
    }

    #Create Message for publish
    pub_message = dict()
    pub_message['DeviceId'] = device_id
    pub_message['Message'] = request_body['Message']
    pub_message['MessageInfo'] = info
    
    pub_message = json.dumps(pub_message) #Convert JSON dict to string.
    
    myAWSIoTMQTTClient.publish(pub_topic, pub_message, 1) #Publish to MQTT

    logger.debug("Publishing message: " + json.dumps(pub_message))
    logger.debug("Waiting for " + thisRequestId)

    event = threading.Event() #Start waiting thread.

    event_Dict[thisRequestId] = event #Save waiting event in Dict, waiting for the response.

    event.wait(timeout=10) #Wait for 10 seconds before time out, or the event being set()

 #   logger.debug("Received the response..")

    response = json.dumps(response_Dict[thisRequestId])

    return response

@app.route('/lambda-response/<device_id>', methods=['POST'])
def response_device(device_id):

    response = json.loads(request.data)

    response_Dict[response['MessageInfo']['RequestId']] = response

    event_Dict[response['MessageInfo']['RequestId']].set()
    
    logger.debug(response)
    return json.loads('{"Status: "200"')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
