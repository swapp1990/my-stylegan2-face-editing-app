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

from flask_socketio import join_room, leave_room

# instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
login = LoginManager(app)
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, async_mode='threading')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
connectedToClient = False
stylegan_encode = None

users = []

class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id

@login.user_loader
def load_user(id):
    return User(id)

def runServer():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

def initApp():
    global connectedToClient
    print('connected ', connectedToClient)
    if not connectedToClient:
        stylegan_encode = sg_encode.StyleGanEncoding()
        threadG = workerCls.Worker(0, stylegan_encode, socketio=socketio)
        threadG.start()
        thread2 = workerCls.Worker(1, socketio=socketio)
        thread2.start()
        msg = {'id': 0, 'action': 'makeModel'}
        workerCls.broadcast_event(msg)
        connectedToClient = True
    else:
        actionData = {'action': 'randomize', 'params': {}}
        print('editAction ', EasyDict(actionData))

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
        print('makemodel')
        msg = {'id': 0, 'action': 'initApp', 'params': {}}
        workerCls.broadcast_event(EasyDict(msg))
    # msg = {'id': 0, 'action': 'makeModel'}
    # workerCls.broadcast_event(msg)
    # initApp()

@socketio.on('get-session')
def get_session():
    print(session)
    emit('refresh-session', {
        'session': session.get('value', ''),
        'user': current_user.id
            if current_user.is_authenticated else 'anonymous'
    })

@socketio.on('set-session')
def set_session(data):
    print(data, request.sid)
    users.append({"user": data['user'], "sid": request.sid})
    print(users)
    stylegan_thread = sg_encode.SGEThread(request.sid)
    threadUser = workerCls.Worker(request.sid, stylegan_thread, socketio=socketio)
    threadUser.start()
    #Send first random img to each client seperately as soon as they login
    msg = EasyDict({'id': request.sid, 'action': 'generateRandomImg', 'params': {}})
    workerCls.broadcast_event(EasyDict(msg))

@socketio.on('test-session')
def test_session(payload):
    print("payload ", payload)
    receipient_id = None
    for u in users:
        if u['user'] == payload['user']:
            receipient_id = u['sid']
    if receipient_id is not None:
        socketio.emit('loggedin', "User logged in " + str(payload['user']), room = receipient_id)

def afterLoginInit():
    
    workerCls.clear()
    threadG = workerCls.Worker(0, stylegan_encode, socketio=socketio)
    threadG.start()
    thread2 = workerCls.Worker(1, socketio=socketio)
    thread2.start()
    msg = {'id': 0, 'action': 'test'}
    workerCls.broadcast_event(msg)

# @socketio.on('initApp')
# def initApp(config):
#     print('initApp ', config)
#     msg = {'id': 0, 'action': 'makeModel'}
#     workerCls.broadcast_event(msg)

@socketio.on('editAction')
def editActions(actionData):
    print('editAction ', EasyDict(actionData))
    msg = EasyDict(actionData)
    msg.id = request.sid
    msg.isTfSession = True
    # print(msg)
    workerCls.broadcast_event(msg)
    
