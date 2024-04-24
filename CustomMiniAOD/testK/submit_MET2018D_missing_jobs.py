import json
import os
import fnmatch

import subprocess


json_path = '/users/alikaan.gueven/analyseNanoAOD/GridPlotter/metadatabase/METData.json'
with open(json_path,'r') as fj:
    d = json.load(fj)

tier = 'CustomMiniAOD'
loc  = 'dir'
label= 'met_2018_d'

data_path = d[tier][loc][label]

f = open(f"/scratch-cbe/users/alikaan.gueven/data/{label}.txt", "w")
for root, dirnames, filenames in os.walk(data_path):
    for filename in fnmatch.filter(filenames, '*.root'):
        f.write('file:')
        f.write(os.path.join(root, filename))
        f.write('\n')
f.close()

f = open(f"/scratch-cbe/users/alikaan.gueven/data/{label}.txt", "r")
print(len(f.readlines()))
f.close()

f = open(f"/scratch-cbe/users/alikaan.gueven/data/{label}.txt", "r")
files_as_lines = f.read().splitlines() 
f.close()

def get_files(file_list, n=1):
    count = 0
    assert n > 0
    while count*n < len(file_list):
        if len(file_list) > (count+1)*n:
            files = file_list[count*n:(count+1)*n]
        else:
            files = file_list[count*n:]
        count += 1
        yield files


# dry_run = True
# debug = True

dry_run = False
debug = False

CONFIGFILE = '/users/alikaan.gueven/AOD_to_nanoAOD/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomNanoAOD/testK/Data_UL18_CustomNanoAOD.py'
JOBNAME = f'{label}'
NTHREADS   = 4
NSUBMIT    = 3
MAXEVENTS  = -1

os.makedirs(f'/scratch-cbe/users/alikaan.gueven/data/{label}/outputs', exist_ok=True)
os.makedirs(f'/scratch-cbe/users/alikaan.gueven/data/{label}/joblogs', exist_ok=True)
os.makedirs(f'/scratch-cbe/users/alikaan.gueven/data/{label}/slurmScripts', exist_ok=True)

for i, files in enumerate(get_files(files_as_lines, NSUBMIT)):
    JOBID = i
    OUTPUTFILE  =  f'/scratch-cbe/users/alikaan.gueven/data/{label}/outputs/nanoAOD_{JOBID}.root'
    INPUTFILES  =  f'/scratch-cbe/users/alikaan.gueven/data/{label}/joblogs/nanoAOD_{JOBID}.txt'
    SBATCHOUT   =  f'/scratch-cbe/users/alikaan.gueven/data/{label}/joblogs/nanoAOD_{JOBID}%j.out'
    SLURMSCRIPT =  f'/scratch-cbe/users/alikaan.gueven/data/{label}/slurmScripts/nanoAOD_{JOBID}.sh'
        
    if dry_run:
        print('\n'.join(files))
        print('------------------')
        print(OUTPUTFILE)
        print('------------------')
        print(INPUTFILES)
        print('------------------')
        # print(f'cmsRun -n {NTHREADS} {CONFIGFILE} inputFiles={INPUTFILES} outputFile={OUTPUTFILE} maxEvents={MAXEVENTS}')
        # print('------------------')
        print('#!/bin/bash')
        print(f'#SBATCH --job-name={JOBNAME}')
        print(f'#SBATCH --output={SBATCHOUT}')
        print(f'#SBATCH --ntasks 1')
        print(f'#SBATCH --cpus-per-task={NTHREADS}')
        print('#SBATCH --mem-per-cpu=2G')
        print('#SBATCH --nodes=1-1')
        print('#SBATCH --partition=c')
        print('#SBATCH --qos=c_short')
        print('#SBATCH --time=08:00:00')
        print('echo JOBID=$SLURM_JOB_ID')
        print('echo -----------------------------------------------')
        print(f'cmsRun -n {NTHREADS} {CONFIGFILE} inputFiles={",".join(files)} outputFile={OUTPUTFILE} maxEvents={MAXEVENTS}')
        print('')
    else:
        with open(INPUTFILES, 'w+') as f:
            f.write('\n'.join(files))
        with open(SLURMSCRIPT, 'w+') as f:
            f.write('#!/bin/bash \n')
            f.write(f'#SBATCH --job-name={JOBNAME} \n')
            f.write(f'#SBATCH --output={SBATCHOUT} \n')
            f.write(f'#SBATCH --ntasks 1 \n')
            f.write(f'#SBATCH --cpus-per-task={NTHREADS} \n')
            f.write('#SBATCH --mem-per-cpu=2G \n')   # memory per cpu-core
            f.write('#SBATCH --nodes=1-1 \n')
            f.write('#SBATCH --partition=c \n')
            f.write('#SBATCH --qos=c_short \n')
            # f.write('#SBATCH  --exclude=clip-g4-10 \n')
           
            f.write('#SBATCH --time=08:00:00 \n')
            f.write('echo ----------------------------------------------- \n')
            
            f.write(f'cmsRun -n {NTHREADS} {CONFIGFILE} inputFiles={",".join(files)} outputFile={OUTPUTFILE} maxEvents={MAXEVENTS}')
        
        subprocess.run(['sbatch', SLURMSCRIPT])
#         with open(SBATCHOUT2, 'w+') as f:
#             subprocess.run(['sbatch', SLURMSCRIPT],stdout=f, stderr=subprocess.STDOUT)
    if debug:
        break


