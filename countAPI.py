from flask import request
from flask import Flask
from flask import json
from flask import send_from_directory
#import json
import subprocess
import sys
import os


UPLOAD_FOLDER = '~/ACC-Lab3/'
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
    
    f = request.files['/theFile']
    f.save('theFile')

    return 

@app.route('/uploads/theFile/', methods=['GET', 'POST'])
def download():
    uploads =  app.config['UPLOAD_FOLDER']
    return Flask.send_from_directory(uploads, "theFile", as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
