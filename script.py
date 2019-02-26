import socket
import subprocess
import os
import json

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

print(relative_URI)

print(url)

output = subprocess.check_output(['curl', url])
data = json.loads(output)

subprocess.call(['export', 'AWS_ACCESS_KEY_ID=', data['AccessKeyId']])
subprocess.call(['export', 'AWS_SECRET_ACCESS_KEY=', data['SecretAccessKey']])
subprocess.call(['export', 'AWS_SESSION_TOKEN=', data['Token']])