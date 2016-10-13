from flask import request
from flask import Flask
from flask import send_file
import subprocess
import sys
import os
from task import allFiles
from task import makeBarchart


UPLOAD_FOLDER = '~/ACC-Lab3/'
def transform(text_file_contents):
    return text_file_contents.replace("=", ",")
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/task/', methods=['GET'])
def task():
    data = subprocess.check_output(["python3","task.py"])
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
    app.run(host='0.0.0.0',debug=True)
