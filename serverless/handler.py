import json
from botocore.vendored import requests
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()

def lambda_handler(event, context):
    # logger.debug(event)
    # print(event)
    # events = event['body']
    message = json.loads(event) #Convert String to Json dict
    endpoint = message['EndPoint'] #Get the web-server endpoint
    req = requests.post(endpoint, json.dumps(event)) #Send POST request to endpoint
    return req.status_code