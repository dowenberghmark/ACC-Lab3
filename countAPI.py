from flask import request
from flask import Flask
from flask import json
#import json
import subprocess
import sys
import os

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

@app.route('/theFile/', methods=['GET', 'POST'])
def download():
    #uploads = os.path.join(current_app.root_path, app.config['./'])
    return send_from_directory('./', filename="theFile")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
