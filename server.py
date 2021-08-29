from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import subprocess
import json


app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
LED_INFO = {
  "processes": [],
  "status": False,
  "brightness": 200,
  "mode": ""
}

@app.route('/led1', methods=['GET'])
@cross_origin()
def get_led_info():
  try:
    return jsonify(
      status=LED_INFO['status'],
      brightness=LED_INFO['brightness'],
      mode=LED_INFO['mode']
    )
  except Exception as e:
    return jsonify(e)

@app.route('/led1', methods=['POST'])
@cross_origin()
def change_led():
  try:
    request_data = request.get_json()

    body = request_data['body']
    body_json = json.dumps(body)
    
    if(request_data['start'] == True):
      if(len(LED_INFO["processes"]) > 0):
        LED_INFO["processes"][-1].kill()

      proc = subprocess.Popen(["python", "./led-scripts/alo1.py", body_json])
      LED_INFO["processes"].append(proc)
      LED_INFO['status'] = True
      LED_INFO['mode'] = body['mode']
      LED_INFO['brightness'] = body['brightness']
      return('open')
    
    if(request_data['start'] == False):
      if(len(LED_INFO["processes"]) > 0): 
        LED_INFO["processes"][-1].kill()
        LED_INFO['status'] = False
        return('closed')
      return('No process to kill')


  except Exception as e:
    print(e)
    return('erorr')


if __name__ == '__main__':
  # run app in debug mode on port 5000
  app.run(debug=True, host='192.168.0.128', port=5000)
