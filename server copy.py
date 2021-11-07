from flask import Flask
from flask import request, jsonify

import subprocess
import json
import os, signal
import random


app = Flask(__name__)
#CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
LED_INFO = {
  "processes": [],
  "status": True,
  "brightness": 200,
  "mode": "",
  "color": 0
}

@app.route('/led1', methods=['GET'])
#@cross_origin()
def get_led_info():
  try:
    return jsonify(
      status=LED_INFO['status'],
      brightness=LED_INFO['brightness'],
      mode=LED_INFO['mode'],
      color=LED_INFO['color']
    )
  except Exception as e:
    return jsonify(e)

@app.route('/led1', methods=['POST'])
#@cross_origin()
def change_led():
  try:
    request_data = request.get_json()
    body = request_data['body']
    body_json = json.dumps(body)
    if(request_data['start'] == True):
      if(len(LED_INFO["processes"]) > 0):
        #LED_INFO["processes"][-1].kill()
        
        #os.kill(LED_INFO["processes"][0].pid, signal.SIGTERM)
     
        LED_INFO["processes"].pop(0)
        #os.system('sudo kill '+str(LED_INFO["processes"][0].pid))
      print('AICI SUNT FRATE', body_json)

     # proc = subprocess.Popen(["sudo", "python3", "./led-scripts/bedroom1.py", body_json], preexec_fn=os.setsid)

  
      LED_INFO["processes"].append({"test": random.randint(0,1000)})
      LED_INFO['status'] = True
      LED_INFO['mode'] = body['mode']
      LED_INFO['brightness'] = body['brightness']
      LED_INFO['color'] = body['color']
      return('open')

    if(request_data['start'] == False):

      if(len(LED_INFO["processes"]) > 0):
        #os.kill(LED_INFO["processes"][0].pid, signal.SIGTERM)
        #os.killpg(os.getpgid(LED_INFO["processes"][0].pid), signal.SIGTERM)
        
        #LED_INFO["processes"][0].kill()
        LED_INFO["processes"].pop()

        #subprocess.Popen(["sudo","python3", "./led-scripts/clear.py", body_json])

        LED_INFO['status'] = False
        return('closed')
      return('No process to kill')

  except Exception as e:
    print(e)
    return (e)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type'
    header['Access-Control-Allow-Methods'] = 'GET,POST'

    return response

if __name__ == '__main__':
  # run app in debug mode on port 5000
  app.run(debug=True, port=5001)
