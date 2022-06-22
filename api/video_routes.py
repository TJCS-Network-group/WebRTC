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


# def process_video(stu_no):
    
#     time.sleep(10)
#     print("process video")
#     global RECORD_DIR
#     DIR = RECORD_DIR + "u" + str(stu_no) + "/"
#     filenames = None
#     for root, dirs, files in os.walk(DIR):
#         filenames = [x for x in files if not 'processed_' in x]
#         break
    
#     cameraVideos = [x for x in filenames if 'origin-video-' in x]
#     screenVideos = [x for x in filenames if 'origin-screen-' in x]
#     if len(screenVideos)==0:
#         return
#     if len(cameraVideos)!=0:
#         cameraVideos.sort()
#         cameraOutput = cameraVideos[0][7:]
#         for file in cameraVideos:
#             command = "ffmpeg -loglevel quiet -y -i " + DIR + file + " -vcodec copy -acodec copy " + DIR + "processed_" + file
#             os.system(command)
#         cameraVideos = [
#             "processed_" + x for x in filenames if 'origin-video-' in x
#         ]
        
#         with open(DIR + "cameralist.txt", 'w') as outfile:
#             for filename in cameraVideos:
#                 outfile.write("file \'" + filename + "\'\n")
#         command = "cd " + DIR + " && ffmpeg -loglevel quiet -y -f concat -i cameralist.txt -c copy " + cameraOutput
#         os.system(command)
    
#         finalCameraOutput = "u" + str(stu_no) + "-" + get_stu_name(
#         stu_no) + "-" + cameraOutput
        
#         os.rename((DIR + cameraOutput).encode('gbk'),
#               (DIR + finalCameraOutput).encode('gbk'))
        
#         os.remove(DIR + "cameralist.txt")
        
#     screenVideos.sort()    
#     screenOutput = screenVideos[0][7:]
    
#     for file in screenVideos:
#         command = "ffmpeg -loglevel quiet -y -i " + DIR + file + " -vcodec copy -acodec copy " + DIR + "processed_" + file
#         os.system(command)
    
#     screenVideos = [
#         "processed_" + x for x in filenames if 'origin-screen-' in x
#     ]    


#     with open(DIR + "screenlist.txt", 'w') as outfile:
#         for filename in screenVideos:
#             outfile.write("file \'" + filename + "\'\n")
    
#     command = "cd " + DIR + " && ffmpeg -loglevel quiet -y -f concat -i screenlist.txt -c copy " + screenOutput
#     os.system(command)
    
#     finalScreenOutput = "u" + str(stu_no) + "-" + get_stu_name(
#         stu_no) + "-" + screenOutput
#     os.rename((DIR + screenOutput).encode('gbk'),
#               (DIR + finalScreenOutput).encode('gbk'))
    
#     for root, dirs, files in os.walk(DIR):
#         removefiles = [x for x in files if 'origin-' in x]
#         break
#     for file in removefiles:
#         os.remove(DIR + file)
#     os.remove(DIR + "screenlist.txt")
#     # print(cameraVideos)
#     # print(finalCameraFname)

def process_video(stu_no,path):
    
    # time.sleep(10)
    print("process video")
    print(path)
    first_index=path.index('origin')
    DIR = path[0:first_index]
    filename = path[first_index:]
    finalName = 'u'+str(stu_no)+ "-" + get_stu_name(stu_no) +filename[6:]
    print(DIR)
    print(filename)
    print(finalName)
    command = "ffmpeg -loglevel quiet -y -i " + DIR + filename + " -vcodec copy -acodec copy " + DIR + "processed_" + filename
    print(command)
    os.system(command)
    os.rename((DIR + "processed_" + filename).encode('gbk'),
              (DIR + finalName).encode('gbk'))
    

# process_video('1950638','/home/webrtc/video/u1950638/origin-screen-2022-06-23-00-45-31.webm')


class RecordManager:

    def __init__(self, account,camera):
        mkdir(RECORD_DIR + "u" + str(account))
        if camera == 'true':
            self.cameraOutputPath = RECORD_DIR + "u" + str(
                account) + "/origin-video-" + datetime.now().strftime(
                    "%Y-%m-%d-%H-%M-%S") + ".webm"
            self.cameraOutput = open(self.cameraOutputPath, "wb")
            self.cameraSemaphore = BoundedSemaphore(1)
        self.screenOutputPath = RECORD_DIR + "u" + str(
            account) + "/origin-screen-" + datetime.now().strftime(
                "%Y-%m-%d-%H-%M-%S") + ".webm"        
        self.screenOutput = open(self.screenOutputPath, "wb")        
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
    camera=request.args.get('camera')
    print(camera,type(camera))
    account = session.get('account')
    
    if AccountMap.get(account) is not None:
        newTread = threading.Thread(target=process_video,args=(session['account'],,))
        newTread.start()
    
    AccountMap[account] = RecordManager(account,camera)
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
    if hasattr(manager,'cameraOutput'):
        manager.cameraOutput.close()
    manager.screenOutput.close()
    AccountMap[account]
    
    return make_response_json(data={"message": "success"})

    manager.cameraSemaphore.acquire()
    manager.screenSemaphore.acquire()
    with open(manager.cameraOutput, 'ab') as output:
        output.write(manager.cameraBuffer)
    with open(manager.screenOutput, 'ab') as output:
        output.write(manager.screenBuffer)
    manager.cameraSemaphore.release()
    manager.screenSemaphore.release()
