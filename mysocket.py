import numpy as np
from flask import Flask, jsonify, request, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_session import Session
from flask_cors import CORS
from flask import Response
from flask_socketio import SocketIO, emit
import mpld3
import logging
from operator import itemgetter
# my classes
from server.threads import Worker as workerCls
import sg_encode
import MyThreads
from easydict import EasyDict
import threading

# instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=True, async_mode='threading')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
connectedToClient = False
stylegan_encode = None

users = []


def runServer():
    users = []
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    workerCls.clear()


@socketio.on('connect')
def connect():
    print("connect")


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
    # print(users.get("user"))

    if threading.active_count() < 50:
        stylegan_thread = MyThreads.ClientThread(request.sid)
        threadUser = workerCls.Worker(
            request.sid, stylegan_thread, socketio=socketio)
        threadUser.start()
        # Send first random img to each client seperately as soon as they login
        # msg = EasyDict({'id': request.sid, 'action': 'setUser', 'params': {'username': data['user']}})
        # workerCls.broadcast_event(EasyDict(msg))
        msg = EasyDict(
            {'id': request.sid, 'action': 'generateRandomImg', 'params': {}})
        workerCls.broadcast_event(EasyDict(msg))
        msg = EasyDict(
            {'id': request.sid, 'action': 'sendStyleMixGallery', 'params': {}})
        workerCls.broadcast_event(EasyDict(msg))
        # #Send chats
        # msg = EasyDict({'id': request.sid, 'action': 'sendChats', 'params': {}})
        # workerCls.broadcast_event(EasyDict(msg))
    else:
        print("cannot start new thread")


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


@app.route("/")
def hello_world():
    return "Test 123 "


def transform_from_list(post_json):
    transformed_payload = {}
    for key in post_json.keys():
        if isinstance(post_json[key], list):
            if key == "images":
                transformed_payload[key] = np.asarray(
                    post_json[key], dtype=np.uint8)
            else:
                transformed_payload[key] = np.asarray(
                    post_json[key], dtype=np.float32)
    return transformed_payload


@app.route("/msgFromColab", methods=['POST'])
def msgFromColab():
    post_json = request.get_json(force=True)
    client_id = post_json["client_id"]
    transformed_payload = transform_from_list(post_json)
    print("msgFromColab ", post_json["action"], transformed_payload.keys())
    msg = EasyDict(
        {'id': client_id, 'action': post_json["action"], 'params': transformed_payload})
    workerCls.broadcast_event(msg)
    return ""
