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


from flask import request
from flask import Flask
from flask import json
from flask import send_from_directory
from flask import send_file

appToCelery = Celery('tasks', backend='amqp', broker='amqp://mast:pass@127.0.0.1/mast_host')


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

matplotlib.use('Agg')

noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}
def countOccurences(f, occurences):
    noRetweetsText = ""
    aTweet = ""
    #flag = True
    #with open(f, 'r+',1) as k:
    for aTweet in (f.splitlines()):
        #print (str(type(aTweet)))
        #print (aTweet)
        if aTweet != '\n' and aTweet != '':
        #    aTweet += letter
        #    flag = True
        #if letter == '\n':# and flag:
        #    flag = False
            formatedTweet = json.loads(aTweet)
            #aTweet = ""
            if not formatedTweet["retweeted"]:
                noRetweetsText = noRetweetsText + (str(formatedTweet["text"]))
    counts = Counter(noRetweetsText.split())
    for find in occurences:    
        occurences[find] = occurences[find] + counts[find]
    
    
    
    

@appToCelery.task()
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
        
     #   target.write(text)
    #target.close()
    #for item in itemContainer:
 #       fileNr = fileNr + 1
#        print ("file: " + str(fileNr)) #+ " name: " + str(item))
        try:
            countOccurences(text, occurences)
        except:
            raise
            #print (occurences)
        gc.collect()
    conn.close()    
    return (occurences)

#allFiles(conn)




@appToCelery.task(ignore_result=True)
def makeBarchart():
    plt.bar(range(len(occurences)), occurences.values(), align='center')
    plt.xticks(range(len(occurences)), occurences.keys())
    plt.savefig("./barchart.png", dpi=150)


UPLOAD_FOLDER = '~/ACC-Lab3/'
def transform(text_file_contents):
    return text_file_contents.replace("=", ",")
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/task/', methods=['GET'])
def task():
    data = allFiles()#subprocess.check_output(["python3","task.py"])
    saveJson = open("./theFile", 'w')
    jsonData = json.dumps(data.decode("utf-8").lower())
    print (data.decode("utf-8").lower())
    saveJson.write(jsonData)
    
    
    #f = request.files['/theFile']
    #f.save(os.path.join(app.config['UPLOAD_FOLDER'], saveJson))
    saveJson.close()
    result = "Result: "+ str(jsonData) + "\n To download the File use:\n curl -o http://130.238.29.82:5000/theFile\n"
    return  (result)#send_file("./theFile", as_attachment= True)

@app.route('/theFile', methods=['GET', 'POST'])
def download():
     return send_file("theFile", as_attachment=True)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
# @app.route('/test/<filename>')
# def dictionary_download (filename):

#     path = os.path.abspath (app.config['TYPO_DICT_PATH'])
#     assert os.path.exists (path)

#     return send_from_directory (path, filename, as_attachment=True,
#         mimetype='application/octet-stream')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
