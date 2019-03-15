from flask import Flask
from flask import request

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

import boto3

import json
import uuid
import subprocess
import requests
import logging
import threading
import sys
    
#test change
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()

app = Flask(__name__)

client = boto3.client('iot-data')

#Config
xray_recorder.configure(
    service='Demo-APP',
    sampling_rules=False
)

XRayMiddleware(app, xray_recorder)

response_Dict = dict()
event_Dict = dict()

#GET IP address of the web-server
endpoint_url = requests.get('http://ip.42.pl/raw').text + "/lambda-response/"

@app.route('/device-request/<device_id>', methods=['POST'])
def request_device(device_id):

    pub_topic = "api/iot/pub/" + device_id

    request_body = json.loads(request.data)

    thisRequestId = str(uuid.uuid4()) #Create new Request ID

    #Create Dictionary containing the info about the webserver
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

    client.publish( #Publish to IoT
        topic= pub_topic,
        qos=0,
        payload=pub_message.encode()
    )    
    
    logger.debug("Publishing message: " + json.dumps(pub_message))
    logger.debug("Waiting for " + thisRequestId)

    event = threading.Event() #Start waiting thread.

    event_Dict[thisRequestId] = event #Save waiting event in Dict, waiting for the response.

    event.wait(timeout=10) #Wait for 10 seconds before time out, or the event being set()

    del event_Dict[thisRequestId]

    #Check if the response_dit contains the request key, if not resposne will be a time-out
    if thisRequestId in response_Dict:
        response = response_Dict[thisRequestId]
        del response_Dict[thisRequestId]
        return json.dumps(response)
    else:
        return '{"Status": "Time-out"}'


@app.route('/lambda-response/<device_id>', methods=['POST'])
def response_device(device_id):

    response = json.loads(request.data)

    response_Dict[response['MessageInfo']['RequestId']] = response

    #Set the waiting thread.
    event_Dict[response['MessageInfo']['RequestId']].set()
    
    return json.loads('{"Status": "200"}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
