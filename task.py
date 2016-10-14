import json
from collections import Counter
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
import gc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from celery import Celery

from flask import Flask
from flask import send_from_directory
from flask import send_file




# _*_ coding:utf-8 _*_
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

UPLOAD_FOLDER = '~/ACC-Lab3/'
noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://mast:pass@130.238.29.82:5000/mast_host',
    CELERY_RESULT_BACKEND='amqp'
)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)

flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@flask_app.route('/countWords', methods=['GET'])
def countWords():
    data = allFiles(conn)#subprocess.check_output(["python3","task.py"])
    saveJson = open("./theFile", 'w')
    jsonData = json.dumps(data.decode("utf-8").lower())
    print (data.decode("utf-8").lower())
    saveJson.write(jsonData)
    
    saveJson.close()
    result = "Result: "+ str(jsonData) + "\n To download the File use:\n curl -o http://130.238.29.82:5000/theFile\n"
    return  (result)#send_file("./theFile", as_attachment= True)

@flask_app.route('/theFile', methods=['GET', 'POST'])
def download():
     return send_file("theFile", as_attachment=True)






def countOccurences(f, occurences):
    noRetweetsText = ""
    aTweet = ""
    #flag = True
    #with open(f, 'r+',1) as k:
    for aTweet in (f.splitlines()):
        if aTweet != '\n' and aTweet != '':

            formatedTweet = json.loads(aTweet)
            #aTweet = ""
            if not formatedTweet["retweeted"]:
                noRetweetsText = noRetweetsText + (str(formatedTweet["text"]))
    counts = Counter(noRetweetsText.split())
    for find in occurences:    
        occurences[find] = occurences[find] + counts[find]
    
@celery.task
def allFiles (conn):
    itemContainer = []
    containerData = conn.get_container("tweets")
    fileNr = 0
    #target = open("./dump.txt", 'a')
    text = ""
    for item in containerData[1]:
        itemContainer.append(item['name'])
        while True :
            try:
                AFile = conn.get_object( container="tweets", obj=item['name'])
                #AFile = subprocess.check_call(["curl","-s" ,"-O", "http://130.238.29.253:8080/swift/v1/tweets/"+ item['name'] ])
                break
            except:
                raise
        text = str(AFile[1].decode("utf-8"))
      
 #       fileNr = fileNr + 1
#        print ("file: " + str(fileNr)) #+ " name: " + str(item))
        try:
            countOccurences(text, occurences)
        except:
            raise

        gc.collect()
    conn.close()    
    return (occurences)







def makeBarchart():
    plt.bar(range(len(occurences)), occurences.values(), align='center')
    plt.xticks(range(len(occurences)), occurences.keys())
    plt.savefig("./barchart.png", dpi=150)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',port=5000 ,debug=True)
