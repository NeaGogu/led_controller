import time
import argparse
import json
import sys
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("body")

args = parser.parse_args()

body = json.loads(args.body)


while True:
  print(body['test'])
  #print(body.get("test"))
  time.sleep(1)