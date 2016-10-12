from flask import request
from flask import Flask
import json
import subprocess
import sys


app = Flask(__name__)

@app.route('/task', methods=['GET', 'POST'])
def task():
    data = subprocess.call(["python3","task.py"])
    saveJson = open("./theFile", 'w')
    jsonData = json.dumps(data)
    saveJson.write(jsonData)
    saveJson.close()
    if request.method == 'POST':
        f = request.files['./theFile']
        f.save('./theFile')
        return ()
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
