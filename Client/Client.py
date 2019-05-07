from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from aws_xray_sdk.core import xray_recorder

import logging
import argparse
import json
import uuid

from RpcHandler import RpcHandler

from threading import Thread
from time import sleep

xray_recorder.configure(
    sampling_rules=False,
    service="Device-App"
)

handler = RpcHandler()

publishTopic = "$aws/rules/ECSIOTRULE"

def publish_response_thread(message):
    #Publish to Basic Ingest
    xray_recorder.begin_segment("Device-App-Segment")
    xray_recorder.begin_subsegment("Device-App-Publish-SubSegment")
    myAWSIoTMQTTClient.publish(publishTopic, message.payload, 0)
    xray_recorder.end_subsegment()
    xray_recorder.end_segment()
    print("message send..")

def response_callback(client, userdata, message):
    #Start Publish thread
    p_thread = Thread(target=publish_response_thread, args=(message,))
    p_thread.start()

def rpc_callback_thread(message):
    rpcResult = handler.rpc_request(message)
    myAWSIoTMQTTClient.publish(publishTopic, rpcResult, 0)
    
def rpc_callback(client,userdata,message):
    rpcThread = Thread(target=rpc_callback_thread, args=(message,))
    rpcThread.start()

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file Path")
parser.add_argument("-d", "--DeviceID", action="store", required=False, dest="DeviceID", default="Standard", help="Device ID for topic details")

args = parser.parse_args()
host = args.host
port = 443
deviceId = args.DeviceID
rootCAPath = args.rootCAPath

#Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
clientId = deviceId
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

messageTopic = "api/iot/pub/" + deviceId
subRpcTopic = "api/iot/rpc" + deviceId

myAWSIoTMQTTClient.subscribe(messageTopic, 0, response_callback)
myAWSIoTMQTTClient.subscribe(subRpcTopic,0,rpc_callback)

#Wait for messages.
while True:
        print("waiting..")
        sleep(1)