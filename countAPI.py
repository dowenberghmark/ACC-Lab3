from flask import request
import json
import subprocess
import sys


app = Flask(__name__)

@app.route('/task', methods=['GET', 'POST'])
def task():
    data = subprocess.call(["python","task.py"])
    saveJson = open("./theFile", 'w')
    saveJson.write(json.dumps(data))
    saveJson.close()
    if request.method == 'POST':
        f = request.files['/theFile']
        f.save('/upload/theFile')
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
