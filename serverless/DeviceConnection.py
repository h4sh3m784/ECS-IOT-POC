import json
import boto3
from botocore.exceptions import ClientError

db = boto3.resource('dynamodb', region_name='eu-west-1')
table = db.Table("ConnectedDevicesTable")

def AddDevice(event):
    response = table.put_item(
        Item ={
            'ID' : event['clientId'],
            'info' : event
        }
    )
    print("put item succeeded")
    print(response)
    return 0

def RemoveDevice(event):
    try:
        response = table.delete_item(
            Key={'ID': event['clientId']}
        )
    except ClientError as e:
        print(str(e))
    else:
        print("delete item succeded")
        print(str(response))

def lambda_handler(event, context):

    eventType = event['eventType']

    if eventType == "connected":
        AddDevice(event)
    elif eventType == "disconnected":
        RemoveDevice(event)

    return "we good"