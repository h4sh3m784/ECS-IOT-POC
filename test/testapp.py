import random


# from flask import Flask
# from flask import request
# from threading import Thread

# app1 = Flask(__name__)
# app2 = Flask(__name__)

# @app1.route('/')
# def index1():
#     return 'Hello World1'

# @app2.route('/')
# def index2():
#     return 'Hello world2'

# def runFlaskApp1():
#     app1.run(host='127.0.0.1', port=5000)

# def runFlaskApp2():
#     app2.run(host='127.0.0.1', port=5001)

# if __name__=='__main__':
#     t1 = Thread(target=runFlaskApp1)
#     t2 = Thread(target=runFlaskApp2)
#     t1.start()
#     t2.start()
for x in range(200):
    print(random.randint(1,6))
