import json
import requests

def lambda_handler(event, context):
    events = event['body']
    message = json.loads(events) #Convert String to Json dict
    endpoint = message['EndPoint'] #Get the web-server endpoint
    req = requests.post(endpoint, json.dumps(events)) #Send POST request to endpoint
    return req.status_code