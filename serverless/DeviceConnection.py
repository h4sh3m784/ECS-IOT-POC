import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

db = boto3.resource('dynamodb', region_name='eu-west-1')
table = db.Table("ConnectedDevicesTable")

def add_device(event):
    #Put new item based on clientId in dynamodb table.
    response = table.put_item(
        Item ={
            'ID' : event['clientId'],
            'versionNumber' : event['versionNumber']
        }
    )
    print("put item succeeded")
    print(response)
    return 0

def remove_device(event):
    #Delete item based on clientId in dnyamodb table.
    try:
        response = table.delete_item(
            Key={'ID': event['clientId']}
        )
    except ClientError as e:
        print(str(e))
    else:
        print("delete item succeded")
        print(str(response))

def is_message_out_of_order(event):
    #get the client id
    id = event['clientId']
    #get the client versionNumber
    versionNumber = event['versionNumber']
    try:
        #query dynamodb table using the client id
        response = table.query(
            KeyConditionExpression=Key('ID').eq(id))
    except ClientError as e:
        print(str(e))
    else:
        #if query was sucessful get the items
        item = response['Items']
        #check if item list is not empty
        if len(item) > 0:
            #get older version of client versionNumber
            old_version_number = item[0]['versionNumber']
            #Compare old with new versionNumber to check if event is not out of order.
            if old_version_number > versionNumber or versionNumber == 0:
                return True
    return False
    

def lambda_handler(event, context):
    eventType = event['eventType']
    #Check if device pressance message is out or order
    if not is_message_out_of_order(event):
        if eventType == "connected":
            add_device(event)
        elif eventType == "disconnected":
            remove_device(event)