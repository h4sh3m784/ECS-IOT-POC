import boto3
import json
import uuid

from flask import Blueprint
from flask import request
from threading import Event
from config import info
from responseHandler import responses

requestView = Blueprint('requestView', __name__)

client = boto3.client('iot-data')

events = dict()

endpoint = info['Endpoint']

def response(id):
    if id in responses: #Check if response arrived
        response = responses[id]
        del responses[id] #Delete response
        return json.dumps(response)
    else:
        return '{"status": "time-out"}'

def wait_for_event(time, id):
    event = Event() #Create new event
    events[requestId] = event #Save the event
    event.wait(timeout=time) #Wait for event to be set() in the responseHandler.py
    del events[id]

def publish_to_topic(topic,message):
    
    id = str(uuid.uuid4())

    message['RequestId'] = id

    message = json.dumps(message)

    client.publish(topic=topic,qos=0,playload=message.encode())

    return id

@requestView.route('/healthcheck',methods=['POST'])
def healthCheck():
    return 'OK'

@requestView.route('/rpc', methods=['POST'])
def requestRPC():

    request = json.loads(request.data)

    topic = "api/iot/rpc" + request['clientId']
    
    id = publish_to_topic(topic, request)

    wait_for_event(60, id)

    return response(id)

@requestView.route('/device/<deviceId>', methods=['POST'])
def requestDevice(deviceId):

    requestBody = json.loads(request.data)

    topic = "api/iot/pub/" + deviceId
    
    message = {
        "DeviceId" : deviceId,
        "Message": requestBody,
        'Endpoint': info['Endpoint'] + deviceId
    }

    id = publish_to_topic(topic, message)
    
    wait_for_event(10,id)

    return response(id)