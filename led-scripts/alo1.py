import time
import argparse
import json
import os


parser = argparse.ArgumentParser()  
parser.add_argument("body")

args = parser.parse_args()

body = json.loads(args.body)
print("ID OF ALO1 ", os.getpid())
print("sugi pula")

while True:
  #print(body)
  #print(body.get("test"))
  time.sleep(1)