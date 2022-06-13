#!/usr/bin/env python3
# -*- coding: gbk -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
# from chat.models import Room,Message,Recent_Chat_List,Meet_List
from app import socketio
from app import database

import json
import os
from threading import BoundedSemaphore

timer = None
recordtime = None
MAX_SIZE_PER_BUFFER = 1 * 1024 * 1024

cameraBuffer = bytes()
screenBuffer = bytes()

cameraOutput = "1.webm"
screenOutput = "2.webm"

cameraSemaphore = BoundedSemaphore(1)
screenSemaphore = BoundedSemaphore(1)


@socketio.on('connect', namespace="/video")
def connect():
    print("connect..")


@socketio.on('disconnect', namespace="/video")
def disconnect():
    print("disconnect...")


@socketio.on('startRecording', namespace="/video")
def startRecording():
    print("start recording")

    if (os.path.isfile(cameraOutput)):
        os.remove(cameraOutput)
    if (os.path.isfile(screenOutput)):
        os.remove(screenOutput)

    global cameraBuffer
    global screenBuffer
    cameraSemaphore.acquire()
    screenSemaphore.acquire()
    cameraBuffer = bytes()
    screenBuffer = bytes()
    cameraSemaphore.release()
    screenSemaphore.release()


@socketio.on('camerablob', namespace="/video")
def receiveCameraBlob(message):
    # print(type(message['blob']))
    global cameraBuffer
    cameraSemaphore.acquire()
    cameraBuffer = cameraBuffer + message['blob']
    cameraSemaphore.release()


@socketio.on('camerablobend', namespace="/video")
def receiveCameraBlobEnd():
    global cameraBuffer
    print(len(cameraBuffer))

    if len(cameraBuffer) > MAX_SIZE_PER_BUFFER:
        cameraSemaphore.acquire()
        with open(cameraOutput, 'ab') as output:
            output.write(cameraBuffer)
        cameraBuffer = bytes()
        cameraSemaphore.release()


@socketio.on('screenblob', namespace="/video")
def receiveScreenBlob(message):
    # print(type(message['blob']))
    global screenBuffer
    screenSemaphore.acquire()
    screenBuffer = screenBuffer + message['blob']
    screenSemaphore.release()


@socketio.on('screenblobend', namespace="/video")
def receiveScreenBlobEnd():
    global screenBuffer
    print(len(screenBuffer))
    if len(screenBuffer) > MAX_SIZE_PER_BUFFER:
        screenSemaphore.acquire()
        with open(screenOutput, 'ab') as output:
            output.write(screenBuffer)
        screenBuffer = bytes()
        screenSemaphore.release()


@socketio.on('endRecording', namespace="/video")
def endRecording():
    print("end recording")
    global cameraBuffer
    global screenBuffer
    cameraSemaphore.acquire()
    screenSemaphore.acquire()
    with open(cameraOutput, 'ab') as output:
        output.write(cameraBuffer)
    with open(screenOutput, 'ab') as output:
        output.write(screenBuffer)
    cameraSemaphore.release()
    screenSemaphore.release()


# def create_or_update_meet_list(sender,receiver):
#     user,created=Meet_List.get_or_create(user_id=sender)
#     meet_list={}
#     if created:
#         meet_list[sender]=[receiver]
#     else:
#         meet_list=user.meet_list
#         if receiver not in meet_list[sender]:
#             meet_list[sender].append(receiver)
#     Meet_List.update(meet_list=meet_list).where(Meet_List.user_id==sender).execute()

# @socketio.on('text', namespace='/chat')
# def text(message):
#     if database.is_closed():
#         database.connect()

#     sender = str(current_user.id)

#     roomid = message['room']

#     state=Room.get_or_none(Room.room_id==roomid)

#     read=0
#     if (state==None):
#         pass
#     elif state.room_state==2:
#         read=1

#     if read==0:
#         if Recent_Chat_List.get_or_none(receiver_id=message['receiver'])==None:
#             Recent_Chat_List.insert(
#             receiver_id=message['receiver'],
#             sender_id=sender,
#             last_time=message['time'],
#             last_msg=message['msg'],
#             unread=1).execute()
#         else:
#             Recent_Chat_List.update(
#             last_time=message['time'],
#             last_msg=message['msg'],
#             unread=Recent_Chat_List.unread+1).where(Recent_Chat_List.receiver_id==message['receiver'] and Recent_Chat_List.sender_id==sender).execute()

#             Recent_Chat_List.update(
#             last_time=message['time'],
#             last_msg=message['msg'],).where(Recent_Chat_List.receiver_id==sender and Recent_Chat_List.sender_id==message['receiver']).execute()

#     Message.create(
#                 msg_time=message['time'],
#                 room_id=roomid,
#                 sender_id=sender,
#                 msg_type=message['type'],
#                 msg_content=message['msg'],
#                 msg_read=read)

#     Room.update(last_message=message['msg'],last_sender_id=sender,msg_type=message['type']).where(Room.room_id==roomid).execute()
#     create_or_update_meet_list(sender,message['receiver'])
#     create_or_update_meet_list(message['receiver'],sender)

#     emit('message', {'sender':sender,
#                      'msg':message['msg'],
#                      'other_user':message['receiver'],
#                      'time':message['time'],
#                      'type':message['type']},
#          room=sender)

#     if (read==1):
#         emit('message', {'sender':sender,
#                         'msg':message['msg'],
#                         'other_user':sender,
#                         'time':message['time'],
#                         'type':message['type']},
#             room=message['receiver'])
#     else:
#         emit('notice', {'sender':sender,
#                         'msg':message['msg'],
#                         'other_user':sender,
#                         'time':message['time'],
#                         'type':message['type']},
#             room=message['receiver'])

#     if not database.is_closed():
#         database.close()

# @socketio.on('left', namespace='/chat')
# def left(message):
#     if database.is_closed():
#         database.connect()
#     sender = str(current_user.id)

#     roomid = message['room']

#     leave_room(sender)
#     Room.update(room_state=Room.room_state-1).where(Room.room_id==roomid).execute()
#     print("-")

#     '''emit('status', {'msg': sender + ' has left the room.'},
#          room=sender)
#     if not database.is_closed():
#         database.close()
