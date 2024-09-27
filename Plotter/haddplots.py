import os,glob
import subprocess
import SoftDisplacedVertices.Samples.Samples as s

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str,
    help='directory of the jobs')
args = parser.parse_args()

if __name__=="__main__":
  for d in os.listdir(args.dir):
    if (d=='input') or (not os.path.isdir(os.path.join(args.dir,d))):
      continue
    njobs = len(glob.glob(os.path.join(args.dir,d,'input','*.txt')))
    nfiles = len(glob.glob(os.path.join(args.dir,d,'*.root')))
    if not nfiles==njobs:
      print("\033[1;31m Not all files are processed. Will hadd whatever if availible.\033[0m")
    targetpath = os.path.join(args.dir,'{0}_hist.root'.format(d))
    if os.path.exists(targetpath):
      print("\033[1;31m File {} already exists! Skipping...\033[0m".format(targetpath))
      continue
    haddcmd = 'hadd {0} {1}/{2}/*.root > {1}/{2}/haddlog.txt'.format(targetpath,args.dir,d)
    print(haddcmd)
    process = subprocess.Popen(haddcmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if (process.returncode!=0):
      print("\033[1;31m Hadd failed! Error message below:\033[0m")
      print(stderr)


