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
#import matplotlib.pyplot as plt

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
    aTweet = ""
    flag = True
    #with open(f, 'r+',1) as k:
    for letter in f:
        if letter != '\n':
            aTweet += letter
            flag = True
        if letter == '\n' and flag:
            flag = False
            formatedTweet = json.loads(aTweet)
            aTweet = ""
            if not formatedTweet["retweeted"]:
                noRetweetsText = noRetweetsText + (str(formatedTweet["text"]))
                counts = Counter(noRetweetsText.split())
                for find in occurences:    
                    occurences[find] = occurences[find] + counts[find]
    
    
    
    


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
        fileNr = fileNr + 1
        #print ("file: " + str(fileNr) + " name: " + str(item))
        try:
            countOccurences(text, occurences)
        except:
            raise
            #print (occurences)
        gc.collect()
    conn.close()    
    print (occurences)

allFiles(conn)






#plt.bar(range(len(occurences)), occurences.values(), align='center')
#plt.xticks(range(len(occurences)), occurences.keys())

#plt.show()
