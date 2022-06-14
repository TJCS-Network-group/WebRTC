#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue

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
import gc

MAX_SIZE_PER_BUFFER = 1 * 1024 * 1024
RECORD_DIR = "webrtc_video/"


class RecordManager:

    def __init__(self, account):
        mkdir(RECORD_DIR + "u" + str(account))
        self.cameraBuffer = bytes()
        self.screenBuffer = bytes()
        self.cameraOutputPath = RECORD_DIR + "u" + str(account) + "/u" + str(
            account) + "-video-" + datetime.now().strftime(
                "%Y-%m-%d-%H-%M-%S") + ".webm"
        self.screenOutputPath = RECORD_DIR + "u" + str(account) + "/u" + str(
            account) + "-screen-" + datetime.now().strftime(
                "%Y-%m-%d-%H-%M-%S") + ".webm"
        self.cameraOutput = open(self.cameraOutputPath, "wb")
        self.screenOutput = open(self.screenOutputPath, "wb")
        self.cameraSemaphore = BoundedSemaphore(1)
        self.screenSemaphore = BoundedSemaphore(1)


AccountMap = {}


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)


@api_blue.route('/video/initialize', methods=['GET'])
def video_initialize():
    account = session.get('account')
    print("initialize..." + account)

    return make_response_json(data={"message": "success"})


@api_blue.route('/video/start_record', methods=['GET'])
def start_record():

    account = session.get('account')
    AccountMap[account] = RecordManager(account)
    print("start recording", account)

    # if(os.path.isfile(manager.cameraOutput)):
    #     os.remove(manager.cameraOutput)
    # if(os.path.isfile(manager.screenOutput)):
    #     os.remove(manager.screenOutput)

    # manager.cameraSemaphore.acquire()
    # manager.screenSemaphore.acquire()
    # manager.cameraBuffer = bytes()
    # manager.screenBuffer = bytes()
    # manager.cameraSemaphore.release()
    # manager.screenSemaphore.release()

    return make_response_json(data={"message": "success"})


@api_blue.route('/video/post_camerablob', methods=['POST'])
def post_camerablob():
    file = request.files.get('file')
    # print(file)
    
    account = session.get('account')
    manager = AccountMap[account]
    file.save(manager.cameraOutput)
    return make_response_json(data={"message": "success"})

    account = session.get('account')
    manager = AccountMap[account]
    manager.cameraSemaphore.acquire()
    manager.cameraBuffer = manager.cameraBuffer
    manager.cameraSemaphore.release() 


@api_blue.route('/video/post_screenblob', methods=['POST'])
def post_screenblob():
    file = request.files.get('file')
    # print(file)
    account = session.get('account')
    manager = AccountMap[account]
    file.save(manager.screenOutput)
    return make_response_json(data={"message": "success"})

    account = session.get('account')
    manager = AccountMap[account]
    manager.screenSemaphore.acquire()
    manager.screenBuffer = manager.screenBuffer
    manager.screenSemaphore.release()


@api_blue.route('/video/end_record', methods=['GET'])
def end_record():
    account = session.get('account')
    print("end recording", account)
    manager = AccountMap[account]
    manager.cameraOutput.close()
    manager.screenOutput.close()
    return make_response_json(data={"message": "success"})

    manager.cameraSemaphore.acquire()
    manager.screenSemaphore.acquire()
    with open(manager.cameraOutput, 'ab') as output:
        output.write(manager.cameraBuffer)
    with open(manager.screenOutput, 'ab') as output:
        output.write(manager.screenBuffer)
    manager.cameraSemaphore.release()
    manager.screenSemaphore.release()
