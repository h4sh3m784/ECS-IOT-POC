import socket
import subprocess
import os

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

print(relative_URI)

print(url)

output = subprocess.check_output(['curl', url])

print(output)

os.environ["AWS_ACCESS_KEY_ID"] = output[b'AccessKeyId']
os.environ["AWS_SECRET_ACCESS_KEY"] = output[b'SecretAccessKey']
os.environ["AWS_SESSION_TOKEN"] = output[b'Token']
