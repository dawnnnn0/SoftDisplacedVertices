#!/usr/bin/env python

### This script takes the job directory and summarizes the job output as a json file

import os
import json
import argparse

import SoftDisplacedVertices.Samples.Samples as sps

parser = argparse.ArgumentParser()
parser.add_argument('--label', help="label of jobs / datasets")
parser.add_argument('--dir', help="directory of jobs")
args = parser.parse_args()

assert os.path.exists(args.dir)

d = {
      args.label:{
        "dataset":{},
        "dir":{},
      },
    }

for s in os.listdir(args.dir):
  valid = False
  try:
    getattr(sps,s)
  except:
    valid = False
  else:
    valid = True
  if valid:
    with open(os.path.join(args.dir,s,"log/jobinfo.json"),'r') as fj:
      info = json.load(fj)
    d[args.label]["dir"][s] = info["output"]

json_name = os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Samples/json/{}'.format(args.label))
if os.path.exists(json_name+'.json'):
  i = 1
  json_name += '_{}'
  while os.path.exists(json_name.format(i)+'.json'):
    i += 1

json_name_new = json_name.format(i)

assert not os.path.exists(json_name_new+'.json')

with open(json_name_new+'.json',"w") as f:
  json.dump(d,f,indent=4)

