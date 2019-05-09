import boto3
import json
import uuid

from flask import Blueprint
from flask import request
from flask import make_response
from threading import Event
from config import info
import responseHandler

requestView = Blueprint('requestView', __name__)

client = boto3.client('iot-data')

events = dict()

endpoint = info['Endpoint']

def response(id):
    if id in responseHandler.responses: #Check if response arrived
        response = responseHandler.responses[id]
        del responseHandler.responses[id] #Delete response
        return json.dumps(response)
    else:
        return '{"status": "time-out"}'

def wait_for_event(time, id):
    event = Event() #Create new event
    events[id] = event #Save the event
    event.wait(timeout=time) #Wait for event to be set() in the responseHandler.py
    del events[id]

def publish_to_topic(topic,message):
    
    id = str(uuid.uuid4())

    message['Endpoint'] = endpoint
    message['RequestId'] = id

    message = json.dumps(message)

    client.publish(topic=topic,qos=0,payload=message.encode())

    return id

def build_cors_response(response):
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', "https://d1gdvmfal4vwsv.cloudfront.net")
    response.headers.add('Access-Control-Allow-Credentials', True)
    return response

@requestView.route('/healthcheck',methods=['POST'])
def healthCheck():
    return 'OK'

@requestView.route('/rpc/<deviceId>', methods=['POST'])
def requestRPC(deviceId):

    requestBody = json.loads(request.data)

    topic = "api/iot/rpc" + deviceId
    
    id = publish_to_topic(topic, requestBody)

    wait_for_event(60, id)

    return build_cors_response(response(id))

@requestView.route('/device/<deviceId>', methods=['POST'])
def requestDevice(deviceId):

    requestBody = json.loads(request.data)

    topic = "api/iot/pub/" + deviceId
    
    id = publish_to_topic(topic, requestBody)
    
    wait_for_event(10,id)

    return response(id)