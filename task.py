import json
from collections import Counter
testString = '/home/owen/Documents/AppliedCloudComputing/Lab3/05cb5036-2170-401b-947d-68f9191b21c6'
#myDict = 

json_data = []
noRetweetsText = ""
occurences = {'han': 0, 'hon': 0, 'hen': 0, 'den': 0,'det': 0,'denna': 0,'denne': 0}
    
with open(testString, 'r') as f:
    for aTweet in f:
        if aTweet != '\n':
            formatedTweet = json.loads(aTweet)
            json_data.append(formatedTweet)
            if not formatedTweet["retweeted"]:
                noRetweetsText = noRetweetsText + (str(formatedTweet["text"]).lower())

        
counts = Counter(noRetweetsText.split())
#print (noRetweetsText)
for find in occurences:    
    occurences[find] =  counts[find]
print (occurences)
