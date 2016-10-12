from flask import request
from flask import Flask
import json
import subprocess
import sys

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")
app = Flask(__name__)

@app.route('/task/', methods=['GET'])
def task():
    data = subprocess.check_output(["python3","task.py"])
    saveJson = open("./theFile", 'w')
    jsonData = json.dumps(str(data.decode("utf-8")).lower())
    print (jsonData)
    saveJson.write(jsonData)
    saveJson.close()
    
    #f = request.files['./theFile']
    #f.save('./theFile')

    return jsonData

@app.route('/')
def test():
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
