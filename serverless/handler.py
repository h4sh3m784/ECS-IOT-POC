import json
from botocore.vendored import requests

def lambda_handler(event, context):
    endpoint = "http://" + event['Endpoint'] #Get the web-server endpoint
    req = requests.post(endpoint, json.dumps(event)) #Send POST request to endpoint
    return req.status_code