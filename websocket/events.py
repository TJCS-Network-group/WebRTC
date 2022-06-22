#!/usr/bin/env python3
# -*- coding: GBK -*-
from concurrent.futures import process
from xml.etree.ElementTree import iselement
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from flask_cors import cross_origin
from datetime import datetime
from api.utils import *
# from chat.models import Room,Message,Recent_Chat_List,Meet_List
from app import socketio
from app import database
from app import scheduler

from api.video_routes import process_video

recordtime = None
# MAX_SIZE_PER_BUFFER = 1*1024*1024
# RECORD_DIR = "webrtc_video/"

OnlineTable = {}
ProcessTable = {}

inExam = False


# students=Student.select(*[Student.id,Student.stu_no]).where(Student.stu_userlevel==User_level.Normal.value)
# for student in students:
#     OnlineTable[student.stu_no] = 0

@scheduler.task('interval', id='check_alive', seconds=10, misfire_grace_time=900)
def check_alive():
    need=[Student.id,Student.stu_no]
    students=Student.select(*need).where(Student.stu_userlevel==User_level.Normal.value)
    for student in students:
        if OnlineTable.get(student.stu_no) is None:
            OnlineTable[student.stu_no] = 0
        OnlineTable[student.stu_no] -= 1
        if OnlineTable[student.stu_no]<0:
            OnlineTable[student.stu_no]=0
        socketio.emit("checkAlive",to=student.stu_no)
    print('alive check executed')
      
      
      
def get_online_table():
    return OnlineTable
      


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

@cross_origin
@socketio.on('connect')
def connect():
    print("connect.."+session['account'])
    OnlineTable[session['account']] = 2
    join_room(session['account'])

@cross_origin
@socketio.on('message')
def message(data):
    print("message"+session['account']+"to"+data['to']+":"+data['type'])
    data['from']=session['account']
    socketio.emit("message",data,to=data['to'])

@cross_origin
@socketio.on('disconnect')
def disconnect():
    print("disconnect..."+session['account'])
    # OnlineTable[session['account']] = 0
    leave_room(session['account'])
    # os._exit(-1)

@cross_origin
@socketio.on('alive')
def get_alive():
    print("alive"+session['account'])
    OnlineTable[session['account']] += 1
    if OnlineTable[session['account']]>2:
        OnlineTable[session['account']]=2

@cross_origin
@socketio.on('getOnlineTable')
def getAliveTable():
    print("get online table "+session['account'])
    socketio.emit("onlineTable",{"onlineTable":get_online_table()},to=session['account'])

@cross_origin
@socketio.on('startExam')
def startExam():
    global inExam
    inExam=True
    need=[Student.id,Student.stu_no]
    students=Student.select(*need).where(Student.stu_userlevel==User_level.Normal.value)
    for student in students:
        socketio.emit("startExam",to=student.stu_no)

@cross_origin
@socketio.on('endExam')
def endExam():
    global inExam
    inExam=False
    need=[Student.id,Student.stu_no]
    students=Student.select(*need).where(Student.stu_userlevel==User_level.Normal.value)
    for student in students:
        socketio.emit("endExam",to=student.stu_no)
    #     newTread = threading.Thread(target=process_video,args=(student.stu_no,))
    #     newTread.start()

@cross_origin
@socketio.on('processVideo')
def processVideo():
    stu_no = session['account']
    newTread = threading.Thread(target=process_video,args=(stu_no,))
    newTread.start()



@cross_origin
@socketio.on('checkInExam')
def checkInExam():
    global inExam
    socketio.emit("inExam",{"inExam":inExam},to=session['account'])
