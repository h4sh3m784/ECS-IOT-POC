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

endpoint = info['Endoint']

@requestView.route('/healthcheck',methods=['POST'])
def healthCheck():
    return 'OK'

@requestView.route('/device/<deviceId', methods=['POST'])
def requestDevice(deviceId):

    pubTopic = info['PublishTopic'] + deviceId

    requestBody = json.loads(request.data)

    requestId = str(uuid.uuid4())

    messageInfo = {
        "Endpoint": info['Endpoint'] + deviceId,
        "RequestId": requestId
    }

    pubMessage = {
        "DeviceId" : deviceId,
        "Message": requestBody,
        "MessageInfo": messageInfo
    }

    pubMessage = json.dumps(pubMessage)

    client.publish(
        topic=pubTopic,
        qos=0,
        payload=pubMessage.encode()
    )
    
    event = Event() #Create new event
    events[requestId] = event #Save the event
    event.wait(timeout=10) #Wait for event to be set() in the responseHandler.py

    del events[requestId] #Delete the event

    if requestId in responses: #Check if response arrived
        response = responses[requestId]
        del responses[requestId] #Delete response
        return json.dumps(response)
    else:
        return '{"status": "time-out"}'