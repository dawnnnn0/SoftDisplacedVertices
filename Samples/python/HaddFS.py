#!/usr/bin/env python

### This script takes the job directory and summarizes the job output as a json file

import os
import json
import argparse
import subprocess

import SoftDisplacedVertices.Samples.Samples as sps

parser = argparse.ArgumentParser()
parser.add_argument('--label', help="label of jobs / datasets")
parser.add_argument('--dir', help="directory of jobs")
args = parser.parse_args()

assert os.path.exists(args.dir)

for s in os.listdir(args.dir):
  valid = False
  try:
    getattr(sps,s)
  except:
    valid = False
  else:
    valid = True
  if not valid:
    print ("Sample {} not registered.".format(s))
  with open(os.path.join(args.dir,s,"log/jobinfo.json"),'r') as fj:
    info = json.load(fj)
  jobd = info["jobdir"]
  fsd = jobd+'/fs/'
  inputfiles = []
  for inf in os.listdir(fsd):
    if 'fs' in inf and '.root' in inf:
      inputfiles.append(fsd+inf)
  haddargs = ['hadd', '-f', fsd+s+'.root'] + inputfiles
  p = subprocess.Popen(args=haddargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = p.communicate()
  assert stderr is None
  open(fsd+s+'.haddlog', 'wt').write(stdout)

  if p.returncode != 0:
    print ('PROBLEM hadding %s' % s)

