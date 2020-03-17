from flask import Flask, jsonify, request, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_session import Session
from flask_cors import CORS
from flask import Response
from flask_socketio import SocketIO, emit
import mpld3
import logging
from operator import itemgetter
#my classes
from server.threads import Worker as workerCls
import sg_encode
from easydict import EasyDict

# instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, async_mode='threading')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
connectedToClient = False
stylegan_encode = None

users = []

def runServer():
    users = []
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    workerCls.clear()

@socketio.on('connect')
def connect():
    print("connect")
    global connectedToClient
    global stylegan_encode
    if not connectedToClient:
        connectedToClient = True
        stylegan_encode = sg_encode.StyleGanEncoding()
        threadG = workerCls.Worker(0, stylegan_encode, socketio=socketio)
        threadG.start()
        msg = {'id': 0, 'action': 'initApp', 'params': {}}
        workerCls.broadcast_event(EasyDict(msg))

@socketio.on('disconnect')
def disconnect():
    print("disconnect ", request.sid)
    global users
    users = [x for x in users if x['sid'] not in [request.sid]]
    msg = EasyDict({'id': request.sid, 'close': 'shutdown', 'params': {}})
    workerCls.broadcast_event(EasyDict(msg))
    print("users ", len(users))

@socketio.on('set-session')
def set_session(data):
    print(data, request.sid)
    if data['user'] != 'anon':
        users.append({"user": data['user'], "sid": request.sid})
    else:
        print('anon')
        return
    print(users)
    stylegan_thread = sg_encode.SGEThread(request.sid)
    threadUser = workerCls.Worker(request.sid, stylegan_thread, socketio=socketio)
    threadUser.start()
    #Send first random img to each client seperately as soon as they login
    msg = EasyDict({'id': request.sid, 'action': 'generateRandomImg', 'params': {}})
    workerCls.broadcast_event(EasyDict(msg))
    #Send saved gallery
    msg = EasyDict({'id': request.sid, 'action': 'sendGallery', 'params': {'init': True}})
    workerCls.broadcast_event(EasyDict(msg))

@socketio.on('editAction')
def editActions(actionData):
    print('editAction ', actionData.keys())
    msg = EasyDict(actionData)
    msg.id = request.sid
    workerCls.broadcast_event(msg)

@socketio.on('chatAction')
def editActions(actionData):
    print('chatAction ', actionData.keys())
    msg = EasyDict(actionData)
    msg.id = request.sid
    workerCls.broadcast_event(msg)
    
