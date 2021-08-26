from flask import Flask
from flask import request
import subprocess
import pickle
import json

app = Flask(__name__)
processes_led1 = []

@app.route('/led1', methods=['GET'])
def change_led():
  try:
    request_data = request.get_json()

    body = json.dumps(request_data['body'])
    
    if(request_data['start'] == 1):
      if(len(processes_led1) > 0):
        processes_led1[-1].kill()
      proc = subprocess.Popen(["python", "./led-scripts/alo1.py", body])
      processes_led1.append(proc)
      return('open')
    
    if(request_data['start'] == 0):
      if(len(processes_led1) > 0): 
        processes_led1[-1].kill()
        return('closed')
      return('No process to kill')


  except Exception as e:
    print(e)
    return('erorr')


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)