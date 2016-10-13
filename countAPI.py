from flask import request
from flask import Flask
from flask import json
from flask import send_from_directory
from flask import send_file
#import json
import subprocess
import sys
import os
from tasks import allFiles
from tasks import makeBarchart


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
    
    
    #f = request.files['/theFile']
    #f.save(os.path.join(app.config['UPLOAD_FOLDER'], saveJson))
    saveJson.close()
    result = "Result: "+ str(jsonData) + "\n To download the File use:\n curl -o http://130.238.29.82:5000/theFile\n"
    return  (result)#send_file("./theFile", as_attachment= True)

@app.route('/theFile', methods=['GET', 'POST'])
def download():
     return send_file("theFile", as_attachment=True)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
# @app.route('/test/<filename>')
# def dictionary_download (filename):

#     path = os.path.abspath (app.config['TYPO_DICT_PATH'])
#     assert os.path.exists (path)

#     return send_from_directory (path, filename, as_attachment=True,
#         mimetype='application/octet-stream')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
