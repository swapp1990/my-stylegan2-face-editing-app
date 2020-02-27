import threading
import queue
active_queues = []
active_threads = []

class Worker(threading.Thread):
    def __init__(self, id, modelCls=None, socketio=None):
        threading.Thread.__init__(self)
        self.mailbox = queue.Queue()
        self.id = id
        self.modelCls = modelCls
        self.socketio = socketio
        print("thread ", self.id)
        active_queues.append(self.mailbox)
        active_threads.append(self)
    
    def run(self):
        while True:
            data = self.mailbox.get()
            if data == 'shutdown':
                return
            if 'action' in data.keys():
                print(self, 'received a message', data['action'], str(data['id']))
                if self.id == data['id']:
                    self.doWork(data)
            elif 'actionData' in data.keys():
                print(self, 'received a message', data['actionData'], str(data['id']))
                if self.id == data['id']:
                    self.doWork(data)
            elif 'log' in data.keys():
                print(self, 'received a message', data['log'], str(data['id']))
                if self.id == data['id']:
                    self.emitLogs(data)

    def doWork(self, payload):
        print("do work ", self.id)
        #If payload params has 'isTfSession' set to True, means the work must be done by the main thread (thread 0) which has the tf sess and the model initialized.
        if 'params' in payload.keys():
            if 'isTfSession' in payload.keys() and payload.isTfSession and payload.id != 0:
                print("do work in main")
                payload.origId = payload.id
                payload.id = 0
                broadcast_event(payload)
            else:
                self.modelCls.doWork(payload)
        else:
            self.emitGeneral(payload)
        # if(self.id == 0):
        #     self.modelCls.doWork(msg)
        # else:
        #     self.emitGeneral(msg)
    
    def emitLogs(self, msg):
        print("emit logs ", msg)
        self.socketio.emit('logs', msg)
    
    def emitGeneral(self, msg):
        # print('emitGeneral ', msg)
        self.socketio.emit('General', msg, room = msg.id)

    def stop(self):
        print("stop ", self.id)
        self.mailbox.put("shutdown")
        self.join()
        
def clear():
    active_queues = []
    for t in active_threads:
        t.stop()
    print("cleared all threads", active_threads)

def broadcast_event(data):
    # print(data)
    for q in active_queues:
        q.put(data)
