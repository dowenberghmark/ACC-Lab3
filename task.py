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

noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}
def countOccurences(f, occurences):
    noRetweetsText = ""
    
    with open(f, 'r+',1) as k:
        for aTweet in k:
            if aTweet != '\n':
                formatedTweet = json.loads(aTweet)
                if not formatedTweet["retweeted"]:
                    noRetweetsText = noRetweetsText + (str(formatedTweet["text"]))
    counts = Counter(noRetweetsText.split())
    for find in occurences:    
        occurences[find] = occurences[find] + counts[find]
    k.close()
    
    
    


def allFiles (conn):
    itemContainer = []
    ocurList = []
    containerData = conn.get_container("tweets")
    fileNr = 0
    for item in containerData[1]:
        itemContainer.append(item['name'])
        try:
            #AFile = conn.get_object( container="tweets", obj=item['name'])
            AFile = subprocess.check_call(["curl","-s" ,"-O", "http://130.238.29.253:8080/swift/v1/tweets/"+ item['name'] ])
        except:
            raise
    conn.close()
    for item in itemContainer:
        fileNr = fileNr + 1
        ocurList.append()
        print ("file: " + str(fileNr) + " name: " + str(item))
        try:
            countOccurences("./" + str(item), occurences)
        except:
            print (occurences)
        gc.collect()
        
    print (occurences)

allFiles(conn)
