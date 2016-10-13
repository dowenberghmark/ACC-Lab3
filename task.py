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



json_data = []
noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}
def countOccurences(f, occurences):
    noRetweetsText = ""
    with open(f, 'r') as k:
        for aTweet in k:
            if aTweet != '\n'  :
                formatedTweet = json.loads(aTweet)
                json_data.append(formatedTweet)
                if not formatedTweet["retweeted"]:
                    noRetweetsText = (str(formatedTweet["text"]).lower())
                    counts = Counter(noRetweetsText.split())
                    for find in occurences:    
                        occurences[find] = occurences[find] + counts[find]
    




def allFiles (conn):
    itemContainer = []
    containerData = conn.get_container("tweets")

    for item in containerData[1]:
        itemContainer.append(item['name'])
        #print (itemContainer[13])
        AFile = conn.get_object( container="tweets", obj=item['name'])
        #AFile = conn.get_object( container="tweets", obj=itemContainer[13])
        target = open("./dump.txt", 'w')
        text = str(AFile[1].decode("utf-8"))
        target.write(text)
        target.close()
        countOccurences("./dump.txt", occurences)
    
        
    print (occurences)

allFiles(conn)
