#!/usr/bin/env python3
# -*- coding: gbk -*-
from api.utils import *
from api import api_blue
from threading import BoundedSemaphore
from api.config_routes import get_config

config = get_config(f"./etc/webrtc-default.conf")
RECORD_DIR = config['root-dir']

def get_stu_name(stu_no):
    students = Student.select(*[Student.id, Student.stu_no, Student.stu_name]
                              ).where(Student.stu_no == str(stu_no))
    return students[0].stu_name


def process_video(stu_no):
    
    time.sleep(10)
    print("process video")
    global RECORD_DIR
    DIR = RECORD_DIR + "u" + str(stu_no) + "/"
    filenames = None
    for root, dirs, files in os.walk(DIR):
        filenames = [x for x in files if not 'processed_' in x]
        break
    
    cameraVideos = [x for x in filenames if 'origin-video-' in x]
    screenVideos = [x for x in filenames if 'origin-screen-' in x]
    if len(cameraVideos)==0 or len(screenVideos)==0:
        return
    cameraVideos.sort()
    screenVideos.sort()
    cameraOutput = cameraVideos[0][7:]
    screenOutput = screenVideos[0][7:]
    # print(cameraOutput)
    # print(screenOutput)
    for file in cameraVideos:
        command = "ffmpeg -loglevel quiet -y -i " + DIR + file + " -vcodec copy -acodec copy " + DIR + "processed_" + file
        # print(command)
        os.system(command)
    for file in screenVideos:
        command = "ffmpeg -loglevel quiet -y -i " + DIR + file + " -vcodec copy -acodec copy " + DIR + "processed_" + file
        # print(command)
        os.system(command)
    cameraVideos = [
        "processed_" + x for x in filenames if 'origin-video-' in x
    ]
    screenVideos = [
        "processed_" + x for x in filenames if 'origin-screen-' in x
    ]
    with open(DIR + "cameralist.txt", 'w') as outfile:
        for filename in cameraVideos:
            outfile.write("file \'" + filename + "\'\n")

    with open(DIR + "screenlist.txt", 'w') as outfile:
        for filename in screenVideos:
            outfile.write("file \'" + filename + "\'\n")
    command = "cd " + DIR + " && ffmpeg -loglevel quiet -y -f concat -i cameralist.txt -c copy " + cameraOutput
    # print(command)
    os.system(command)
    command = "cd " + DIR + " && ffmpeg -loglevel quiet -y -f concat -i screenlist.txt -c copy " + screenOutput
    # print(command)
    os.system(command)
    for root, dirs, files in os.walk(DIR):
        filenames = [x for x in files if not 'processed_' in x]
        print(filenames)
        break
    
    finalCameraOutput = "u" + str(stu_no) + "-" + get_stu_name(
        stu_no) + "-" + cameraOutput
    # print("rename",(DIR + cameraOutput).encode('gbk'),
    #           (DIR + finalCameraOutput).encode('gbk'))
    os.rename((DIR + cameraOutput).encode('gbk'),
              (DIR + finalCameraOutput).encode('gbk'))
    finalScreenOutput = "u" + str(stu_no) + "-" + get_stu_name(
        stu_no) + "-" + screenOutput
    # print("rename",(DIR + screenOutput).encode('gbk'),
    #           (DIR + finalScreenOutput).encode('gbk'))
    os.rename((DIR + screenOutput).encode('gbk'),
              (DIR + finalScreenOutput).encode('gbk'))
    
    for root, dirs, files in os.walk(DIR):
        removefiles = [x for x in files if 'origin-' in x]
        break
    for file in removefiles:
        os.remove(DIR + file)
    os.remove(DIR + "cameralist.txt")
    os.remove(DIR + "screenlist.txt")
    # print(cameraVideos)
    # print(finalCameraFname)


class RecordManager:

    def __init__(self, account):
        mkdir(RECORD_DIR + "u" + str(account))
        self.cameraBuffer = bytes()
        self.screenBuffer = bytes()
        self.cameraOutputPath = RECORD_DIR + "u" + str(
            account) + "/origin-video-" + datetime.now().strftime(
                "%Y-%m-%d-%H-%M-%S") + ".webm"
        self.screenOutputPath = RECORD_DIR + "u" + str(
            account) + "/origin-screen-" + datetime.now().strftime(
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
