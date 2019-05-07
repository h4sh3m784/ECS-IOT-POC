import json
import threading

from CallOptions import calls
from uuid import uuid4

import logging

class RpcHandler:

    def __init__(self):

        logging.basicConfig(level=logging.DEBUG)

        self.result = {}
        self.que = []
        self.processing = []

        self.exitProgram = False

        #Start new threading to process the request in the que.
        processThread = threading.Thread(target=self.process_rpc_calls, args=[])
        processThread.start()


    def rpc_request(self, request):
        
        #Add request to the que.
        result = self.add_rpc_que(request)

        #Check if result is an event, else it is an error.
        if isinstance(result,threading.Event):
            return result
        
        #Wait for the process to finish
        result.wait()
        #Remove the process
        del self.processing[0]
        #Get the process result
        return self.request_result()

    def process_rpc_calls(self):
        while not self.exitProgram:
            
            #Check if the main thread is still alive, if not, it will exit the loop.
            self.is_main_thread_alive()

            #Check if the que is not empty
            if(len(self.que) > 0):
                
                #Get the first request in the que
                request = self.que[0]

                id = request['info']['id']
                event = request['info']['event']

                #Check if the request is not already being processed
                if id not in self.processing:
                    #Remove the request from que
                    del self.que[0]
                    #Add to the processing list
                    self.processing.append(id)
                    #Start call execution
                    self.result[id] = self.handle_rpc_call(request)
                    #After call execution if finished, set the event.
                    event.set()
    
    def handle_rpc_call(self, request):
        
        #Check if everything goes correct inside the call function
        try:
            func = request['Call']['function']
            param = request['Call']['parameters']
            if func in calls:
                return calls[func](param)
            else:
                return self.error("function does not exist..")
        except Exception as e:
            return self.error(e)

    def add_rpc_que(self,request):

        try:

            #Check if json string is correct
            #And contains everything needed

            logging.debug(request)
            requestDict = json.loads(request)

            if 'Call' in requestDict:
                if 'function' in requestDict['Call']:
                    if requestDict['Call']['function'] == '':
                        return self.error('function key is empty in json')
                else:
                    return self.error('no function key in json')
                if 'parameters' in requestDict['Call']:
                    if requestDict['Call']['parameters'] == '':
                        return self.error('parameters key is empopty in json')
                else: 
                    return self.error("no parameters keys in json")
            else: return self.error("No Call key in json")

        except Exception as e:
            return self.error(e)

        #Create id and event, add them to the request dictionary
        id = str(uuid4())
        event =  threading.Event()
        request['info'] = {'id': id, "event" : event}

        #Add request to the que
        self.que.append(request)

        return event


    def request_result(self):
        #Get the result in json string: Key -> id, Value -> call result
        #And remove the result key,value
        return json.dumps(dict([self.result.popitem()]))

    def error(self, message):
        return json.dumps({"error:" : str(message)})

    def is_main_thread_alive(self):
            for i in threading.enumerate():
                if i.name == "MainThread":
                    if not i.is_alive():
                        self.exitProgram = True

