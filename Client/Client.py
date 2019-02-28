from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import argparse
import json
import uuid

from threading import Thread
from time import sleep

#Publish Thread
def publish_thread(message):
    message_dic = json.loads(message.payload)
    pub_topic = message_dic['Pub-Topic']
    myAWSIoTMQTTClient.publish(pub_topic, message.payload, 1)
    print(pub_topic)
    print("message send..")

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    #Start Publish thread
    p_thread = Thread(target=publish_thread, args=(message,))
    p_thread.start()

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file Path")
parser.add_argument("-d", "--DeviceID", action="store", required=False, dest="DeviceID", default="Standard", help="Device ID for topic details")

args = parser.parse_args()
host = args.host
port = 443
deviceId = args.DeviceID
rootCAPath = args.rootCAPath

sub_topic = "api/iot/pub/" + deviceId

#Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
clientId = "Client_" + str(uuid.uuid4())
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
myAWSIoTMQTTClient.subscribe(sub_topic, 1, customCallback)

#Wait for messages.
while True:
        print("waiting for message")
        print("On topic: ", sub_topic)
        sleep(1)