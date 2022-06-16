#!/usr/bin/env python3
# -*- coding: GBK -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
# from chat.models import Room,Message,Recent_Chat_List,Meet_List
from app import socketio
from app import database
from datetime import datetime
import json
import os
from threading import BoundedSemaphore


timer = None
recordtime = None
MAX_SIZE_PER_BUFFER = 1*1024*1024
RECORD_DIR = "webrtc_video/"




class RecordManager:
    def __init__(self,account):
        mkdir(RECORD_DIR+"u"+str(account))
        self.cameraBuffer=bytes()
        self.screenBuffer=bytes()
        self.cameraOutputPath = RECORD_DIR+"u"+str(account)+"/u"+str(account)+"-video-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".webm"
        self.screenOutputPath = RECORD_DIR+"u"+str(account)+"/u"+str(account)+"-screen-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".webm"
        self.cameraOutput = open(self.cameraOutputPath,"wb")
        self.screenOutput = open(self.screenOutputPath,"wb")
        self.cameraSemaphore = BoundedSemaphore(1)
        self.screenSemaphore = BoundedSemaphore(1)
        self.lst_camera = 0
        self.lst_screen = 0  
        

AccountMap = {}

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)



@socketio.on('connect', namespace="/video_socket")
def connect():
    print("connect..")

@socketio.on('disconnect', namespace="/video_socket")
def disconnect():
    print("disconnect..."+session.get('account'))
    # os._exit(-1)

@socketio.on('initialize', namespace="/video_socket")
def initialize():
    account = session.get('account')
    print("initialize..."+account)    

    

@socketio.on('startRecording', namespace="/video_socket")
def startRecording():
    account = session.get('account')
    AccountMap[account]=RecordManager(account)
    manager=AccountMap[account]
    print("start recording",account)
    

    # manager.cameraSemaphore.acquire()
    # manager.screenSemaphore.acquire()
    manager.cameraBuffer = bytes()
    manager.screenBuffer = bytes()
    # manager.cameraSemaphore.release()
    # manager.screenSemaphore.release()



@socketio.on('camerablob', namespace="/video_socket")
def receiveCameraBlob(message):
    # print(type(message['blob']))
    account = session.get('account')
    manager=AccountMap[account]
    # manager.cameraSemaphore.acquire()
    manager.cameraBuffer = manager.cameraBuffer + message['blob']
    # manager.cameraSemaphore.release()


@socketio.on('camerablobend', namespace="/video_socket")
def receiveCameraBlobEnd():
    
    account = session.get('account')
    manager=AccountMap[account]
    # print("camera",len(manager.cameraBuffer))

    if len(manager.cameraBuffer) > MAX_SIZE_PER_BUFFER:
        # manager.cameraSemaphore.acquire()
        manager.cameraOutput.write(manager.cameraBuffer)
        manager.cameraBuffer = bytes()
        # manager.cameraSemaphore.release()



@socketio.on('screenblob', namespace="/video_socket")
def receiveScreenBlob(message):
    account = session.get('account')
    manager=AccountMap[account]
    # manager.screenSemaphore.acquire()
    manager.screenBuffer = manager.screenBuffer + message['blob']
    # manager.screenSemaphore.release()



@socketio.on('screenblobend', namespace="/video_socket")
def receiveScreenBlobEnd():
    account = session.get('account')
    manager=AccountMap[account]
    print("screen",len(manager.screenBuffer)-manager.lst_screen)
    if len(manager.screenBuffer) > MAX_SIZE_PER_BUFFER:
        # manager.screenSemaphore.acquire()
        manager.screenOutput.write(manager.screenBuffer)
        manager.screenBuffer = bytes()
        # manager.screenSemaphore.release()
        
    manager.lst_screen = len(manager.screenBuffer)

    



@socketio.on('endRecording', namespace="/video_socket")
def endRecording():
    account = session.get('account')
    print("end recording",account)
    manager=AccountMap[account]
    # manager.cameraSemaphore.acquire()
    # manager.screenSemaphore.acquire()
    manager.cameraOutput.write(manager.cameraBuffer)
    manager.screenOutput.write(manager.screenBuffer)
    # manager.cameraSemaphore.release()
    # manager.screenSemaphore.release()
    manager.cameraOutput.close()
    manager.screenOutput.close()


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
