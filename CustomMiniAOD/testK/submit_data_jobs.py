import os
import subprocess



tier = 'CustomMiniAOD'
label= 'met_2018_d_missingfiles_part3'

path_to_missingFilesList = '/users/alikaan.gueven/tmp/missingFilesRun2018D_part3.txt'

with open(path_to_missingFilesList) as fRead:
    missingFiles = fRead.readlines()
    missingFiles = [f[:-1] for f in missingFiles]



with open(f"/scratch-cbe/users/alikaan.gueven/{label}.txt", "w") as fWrite:
    for file in missingFiles:
        fWrite.write('file:/eos/vbc/experiments/cms')
        fWrite.write(file)
        fWrite.write('\n')

with open(f"/scratch-cbe/users/alikaan.gueven/{label}.txt", "r") as f:
    missingFiles = f.read().splitlines()


with open(f"/scratch-cbe/users/alikaan.gueven/{label}.txt", "r") as f:
    print("Num files: ", len(f.readlines()))



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

CONFIGFILE = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/Data_UL18_CustomMiniAOD.py'
JOBNAME = f'{label}'
NTHREADS   = 4
NSUBMIT    = 1
MAXEVENTS  = -1

os.makedirs(f'/scratch-cbe/users/alikaan.gueven/{label}/outputs', exist_ok=True)
os.makedirs(f'/scratch-cbe/users/alikaan.gueven/{label}/joblogs', exist_ok=True)
os.makedirs(f'/scratch-cbe/users/alikaan.gueven/{label}/slurmScripts', exist_ok=True)

for i, files in enumerate(get_files(missingFiles, NSUBMIT)):
    JOBID = i
    OUTPUTFILE  =  f'/scratch-cbe/users/alikaan.gueven/{label}/outputs/miniAOD_{JOBID}.root'
    INPUTFILES  =  f'/scratch-cbe/users/alikaan.gueven/{label}/joblogs/miniAOD_{JOBID}.txt'
    SBATCHOUT   =  f'/scratch-cbe/users/alikaan.gueven/{label}/joblogs/miniAOD_{JOBID}_%j.out'
    SLURMSCRIPT =  f'/scratch-cbe/users/alikaan.gueven/{label}/slurmScripts/miniAOD_{JOBID}.sh'
        
    if dry_run:
        print('FILES TO PROCESS: ', '\n'.join(files))
        print('------------------')
        print('OUTPUTFILE: ', OUTPUTFILE)
        print('------------------')
        print('INPUTFILES: ', INPUTFILES)
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
        print('#SBATCH --qos=c_long')
        print('#SBATCH --time=13-00:00:00')
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
            f.write('#SBATCH --qos=c_long \n')
            # f.write('#SBATCH  --exclude=clip-g4-10 \n')
           
            f.write('#SBATCH --time=13-00:00:00 \n')
            f.write('echo ----------------------------------------------- \n')
            
            f.write(f'cmsRun -n {NTHREADS} {CONFIGFILE} inputFiles={",".join(files)} outputFile={OUTPUTFILE} maxEvents={MAXEVENTS}')
        
        subprocess.run(['sbatch', SLURMSCRIPT])
#         with open(SBATCHOUT2, 'w+') as f:
#             subprocess.run(['sbatch', SLURMSCRIPT],stdout=f, stderr=subprocess.STDOUT)
    if debug:
        break