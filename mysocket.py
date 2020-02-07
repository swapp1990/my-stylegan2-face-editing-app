from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import Response
from flask_socketio import SocketIO, emit
import mpld3
import logging
#my classes
from server.threads import Worker as workerCls
import sg_encode
import EasyDict as ED

# instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, async_mode='threading')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def runServer():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

@socketio.on('connect')
def connect():
    print('connected')
    stylegan_encode = sg_encode.StyleGanEncoding()
    threadG = workerCls.Worker(0, stylegan_encode, socketio=socketio)
    threadG.start()
    thread2 = workerCls.Worker(1, socketio=socketio)
    thread2.start()

    msg = {'id': 0, 'action': 'makeModel'}
    workerCls.broadcast_event(msg)

@socketio.on('initApp')
def initApp(config):
    print('initApp ', config)
    msg = {'id': 0, 'action': 'makeModel'}
    workerCls.broadcast_event(msg)

@socketio.on('editAction')
def editActions(actionData):
    print('editAction ', ED.EasyDict(actionData))
    actions_kwargs = ED.EasyDict()
    actions_kwargs.id = 0
    actions_kwargs.actionData = ED.EasyDict(actionData)
    workerCls.broadcast_event(actions_kwargs)
