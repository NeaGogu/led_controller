import time
import argparse
import json


parser = argparse.ArgumentParser()  
parser.add_argument("body")

args = parser.parse_args()

body = json.loads(args.body)


while True:
  print(body)
  #print(body.get("test"))
  time.sleep(1)