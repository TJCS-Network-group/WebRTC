#!/usr/bin/env python3
# -*- coding: gbk -*-

#��������
import config

database_name = config.database_name
password = config.password
user = config.user
port = config.port
host = config.host
#��pymysql�������ݿ�
from . import create_database
if config.drop_database==True:
    create_database.create_database(database_name, password, user, host, "gbk")

#����app
from flask import Flask

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = 'b8a0e5e48f7e4577a020b8502dcb7fc8'  #������ɵ���Կ
app.config['JSON_AS_ASCII'] = False

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

from flask_cors import CORS
CORS(app, supports_credentials=True)

from flask_apscheduler import APScheduler
scheduler = APScheduler()
scheduler.init_app(app=app)
scheduler.start()


from flask_socketio import SocketIO

# socketio = SocketIO()
socketio = SocketIO(cors_allowed_origins='*')
socketio.init_app(app)
# socketio = SocketIO(app, cors_allowed_origins="*")




import peewee as pw
# py_peewee���ӵ����ݿ���:database
database = pw.MySQLDatabase(database=database_name,
                            host=host,
                            user=user,
                            passwd=password,
                            charset='utf8',
                            port=port)


class BaseModel(pw.Model):

    class Meta:
        database = database  # ��ʵ�������ݿ���а�


# �������ݿ�
database.connect()

from user import user_blue
from api import api_blue
from websocket import websocket_blue

app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(api_blue, url_prefix='/api')
app.register_blueprint(websocket_blue, url_prefix='/websocket')
#��ʼ�����ݿ�
from . import init_database

init_database.init_database(config.drop_database)

#appĿ¼��·��
from . import routes
