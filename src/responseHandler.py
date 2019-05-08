import json
import requestHandler

from flask import Blueprint
from flask import request
import logging

logging.basicConfig(level=logging.BASIC_FORMAT)

responseView = Blueprint('responseView', __name__)

responses = dict()

@responseView.route('/lambda-response', methods=['POST'])
def responseDevice():
    response = json.loads(request.data)
    key = response['RequestId']
    if key in requestHandler.events: #Check if event hasn't time-out
        responses[key] = response #Save response
        requestHandler.events[key].set() #Set the waiting event
    return '{"status": "200"}'