from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/led1', methods=['GET'])
def change_led():
  request_data = request.get_json()
  #request_query = request.args
  print('aloooo', request.args)
  return (request_data)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)