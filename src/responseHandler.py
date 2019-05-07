import json

from flask import Blueprint
from flask import request
from requestHandler import events

responseView = Blueprint('responseView', __name__)

responses = dict()

@responseView.route('/lambda-response/<deviceId', methods=['POST'])
def responseDevice(deviceId):

    response = json.loads(request.data)

    key = response['MessageInfo']['RequestId']

    if key in events: #Check if event hasn't time-out
        responses[key] = response #Save response
        events[key].set() #Set the waiting event
    return '{"status": "200"}'