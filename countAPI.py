from flask import request
from flask import Flask
from flask import send_file
import subprocess
import sys
import os
from task import allFiles
from  swiftclient import client
from swiftclient import service
import subprocess
import time, os, sys
import inspect
from os import environ as env
import keystoneclient.v3.client as ksclient
from keystoneauth1.identity import v3
from keystoneauth1 import loading
from keystoneauth1 import session
import os.path
#from task import makeBarchart

_authurl = env['OS_AUTH_URL']
_auth_version = '3'
_user = env['OS_USERNAME']
_key = env['OS_PASSWORD']
_os_options = {
    'user_domain_name': env['OS_USER_DOMAIN_NAME'],
    'project_domain_name': env['OS_PROJECT_DOMAIN_NAME'],
    'project_name': env['OS_PROJECT_NAME']
}

conn = client.Connection(
    authurl=_authurl,
    user=_user,
    key=_key,
    os_options=_os_options,
    auth_version=_auth_version
)
flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='rpc://'
)



@flask_app.route('/countWords', methods=['GET'])
def countWords(conn):
    data = allFiles()
    saveJson = open("./theFile", 'w')
    jsonData = json.dumps(data.decode("utf-8").lower())
    print (data.decode("utf-8").lower())
    saveJson.write(jsonData)
    
    saveJson.close()
    result = "Result: "+ str(jsonData) + "\n To download the File use:\n curl -o http://130.238.29.82:5000/theFile\n"
    return  (result)

@app.route('/theFile', methods=['GET', 'POST'])
def download():
     return send_file("theFile", as_attachment=True)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
