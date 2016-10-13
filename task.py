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


#NOTE: add exception for trying to download
json_data = []
noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}
def countOccurences(f, occurences):
    noRetweetsText = ""
    #aTweet = ""
    
    with open(f, 'r') as k:
    #print ("i'm to big for tweet")
        for aTweet in k:
            #print (aTweet)
        # if letter != '\n'  :
        #     aTweet += letter
        #     counter = 0
            if aTweet != '\n':# and counter == 0:
                counter = 1
                
                formatedTweet = json.loads(aTweet)
                json_data.append(formatedTweet)
                if not formatedTweet["retweeted"]:
                    noRetweetsText = noRetweetsText + (str(formatedTweet["text"]))
    counts = Counter(noRetweetsText.split())
    for find in occurences:    
        occurences[find] = occurences[find] + counts[find]
                    #break
            #print (occurences)
        k.close()
    




def allFiles (conn):
    itemContainer = []
    containerData = conn.get_container("tweets")
    fileNr = 0
    for item in containerData[1]:
        
        itemContainer.append(item['name'])
        #print (itemContainer[13])
        #while True:
        try:
            #AFile = conn.get_object( container="tweets", obj=item['name'])
            AFile = subprocess.check_call(["curl","-s" ,"-O", "http://130.238.29.253:8080/swift/v1/tweets/"+ item['name'] ])
            #break
        except:
            raise
                #AFile = conn.get_object( container="tweets", obj=itemContainer[13])
        #print ("Working on File number: " + str(fileNr))
        #target = open(item['name'], 'w')
        #text = str(target.decode("utf-8"))
        
        #target.write(text)

        #target.close()
    for item in itemContainer:
        fileNr = fileNr + 1
        print ("file: " + str(fileNr))
        countOccurences("./" + str(item), occurences)
        gc.collect()
        #print (occurences)
        #subprocess.call(["rm", item['name'] ])
        #break
        
        
    print (occurences)

allFiles(conn)
