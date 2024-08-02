# Example usage:
# python3 autoplotter.py --sample stop_M600_580_ct2_2018 --output ./ --config /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plotconfig_sig.yaml --lumi 59683. --json MLNanoAOD.json --metadata metadata_CustomMiniAOD_v3.yaml --datalabel MLNanoAODv2

import os
import uuid
import shutil
import SoftDisplacedVertices.Plotter.plotter as p
import SoftDisplacedVertices.Plotter.plot_setting as ps
import SoftDisplacedVertices.Samples.Samples as s

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sample', type=str, nargs='+',
                        help='samples to process')
parser.add_argument('--output', type=str,
                        help='output dir')
parser.add_argument('--config', type=str,
                        help='config to use') 
parser.add_argument('--lumi', type=float, default=59683.,
                        help='luminosity to normalise MC samples')
parser.add_argument('--json', type=str, 
                        help='json for file paths') 
parser.add_argument('--metadata', type=str,default='',
                        help='metadata for sum gen weights of MC samples') 
parser.add_argument('--datalabel', type=str,
                        help='datalabel to use in json file') 
parser.add_argument('--data', action='store_true', default=False,
                        help='Whether the input is data') 
parser.add_argument('--submit', action='store_true', default=False,
                        help='Whether to scale the plot')
args = parser.parse_args()


if __name__=="__main__":

  all_samples = []
  for samp in args.sample:
    s_samp = getattr(s,samp)
    if isinstance(s_samp, list): 
      all_samples += s_samp
    else:
      all_samples.append(s_samp)

  if args.submit:
    assert (not os.path.exists(args.output)),"Path {} already exists!".format(args.output)
    os.makedirs(args.output)
    inputdir = args.output+'/input'
    os.makedirs(inputdir)
    shutil.copy2(args.config,inputdir)
    shutil.copy2(os.path.join(os.getcwd(),'autoplotter.py'),inputdir)
    jobf = open('jobs.sh',"w")
    if args.data:
      data = '--data'
    else:
      data=''
    for samp in all_samples:
      uuid_ =  str(uuid.uuid4())
      command = "mkdir /tmp/%s;" % (uuid_)
      command += "cd /tmp/%s;" %(uuid_)
      command += "cp %s /tmp/%s/.;" %(inputdir+'/*',uuid_)
      #command += "cp %s /tmp/%s/.;" %(os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Plotter/autoplotter.py'),uuid_)
      #command += "python3 autoplotter.py --sample {} --output ./ --config {};".format(samp.name,args.config)
      if args.metadata=='':
        command += "python3 autoplotter.py --sample {} --output ./ --config ./{} --lumi {} --json {} --datalabel {} {};".format(samp.name,os.path.basename(args.config),args.lumi,args.json,args.datalabel,data)
      else:
        command += "python3 autoplotter.py --sample {} --output ./ --config ./{} --lumi {} --json {} --metadata {} --datalabel {} {};".format(samp.name,os.path.basename(args.config),args.lumi,args.json,args.metadata,args.datalabel, data)
      command += "cp ./*.root {}/.;".format(args.output)
      command += "\n"
      jobf.write(command)
    jobf.close()

  else:
    lumi = args.lumi # units in pb-1
    #label = "MLNanoAODv2"
    #input_json = "MLNanoAOD.json"
    #info = "metadata_CustomMiniAOD_v3.yaml"
    s.loadData(all_samples,os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Samples/json/{}'.format(args.json)),args.datalabel)
    info_path = os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Samples/json/{}'.format(args.metadata))

    plotter = p.Plotter(datalabel=args.datalabel,outputDir=args.output,lumi=lumi,info_path=info_path,config=args.config,isData=args.data)

    for sample in all_samples:
      plotter.setSample(sample)
      plotter.makeHistFiles()
