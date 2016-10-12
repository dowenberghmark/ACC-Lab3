from flask import Flask, jsonify
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
    if Flask.method == 'POST':
        f = Flask.files['./theFile']
        f.save('/var/www/uloads/theFile')
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
