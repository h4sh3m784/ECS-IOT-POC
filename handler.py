import json
import requests

def lambda_handler(event, context):
    events = event['body']
    message = json.loads(events)
    endpoint = message['EndPoint']
    req = requests.post(endpoint, json.dumps(events))
    return req.status_code