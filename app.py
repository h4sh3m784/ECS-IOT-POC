from flask import Flask
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import json
import uuid
import os
import subprocess
import time

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

output = subprocess.check_output(['curl', url])

data = json.loads(output)

os.environ["AWS_ACCESS_KEY_ID"] = data['AccessKeyId']
os.environ["AWS_SECRET_ACCESS_KEY"] = data['SecretAccessKey']
os.environ["AWS_SESSION_TOKEN"] = data['Token']

app = Flask(__name__)

host = "a29zo009haxq0r-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
sub_topic = "WebInterface/iot/sub"
port = 443

response = {"Status": "200"}

myAWSIoTMQTTClient = AWSIoTMQTTClient(str(uuid.uuid4()), useWebsocket=True)
myAWSIoTMQTTClient.configureEndpoint(host,port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(25)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
myAWSIoTMQTTClient.connect()


def callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    global response
    response = {"Status": "SUCH GOOD MEME"}

    callback.has_been_called = True


callback.has_been_called = False


@app.route('/device/<device_id>', methods=['GET', 'POST'])
def publish_to_iot(device_id):

    pub_topic = "Webinterface/iot/pub/" + device_id

    pub_message = dict()
    pub_message['DeviceId'] = device_id
    pub_message = json.dumps(pub_message)

    myAWSIoTMQTTClient.subscribe(sub_topic, 0, callback)

    myAWSIoTMQTTClient.publish(pub_topic, pub_message, 0)

    time_out = False
    counter = 0

    global response

    while not callback.has_been_called and time_out:
        counter += 1
        if counter >= 10:
            time_out = True
            response = {"Status": "Time-out"}
        time.sleep(1)

    response = json.dumps(response)

    print("---callback log---")
    print(time_out)
    print(callback.has_been_called)

    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
