Guide to using SampleGeneration

**IMPORTANT:** Change directories in the following locations:
- in submit.py the variable wdir should be set to the location where you want to run all jobs (logfiles will be saved there)
- in /templates/job_template.sh the variable STORE should be set to the location where you want to store the resulting .root files

There are two python scripts which are used to operate the signal generation process:
- driver.py
- submit.py

The driver.py file is a wrapper to create the config files needed for cmsRun, while the role of
submit.py is to submit the job file that executes all the cmsRun commands. There are multiple parameters that can be used:
- llpmass (m): mass of the llp, default is 600
- lspmass (l): mass of the lsp, default is 588
- ctau (c): lifetime of the stop, default is 200
- nevents (n): number of simulated events, default is 5000

**Make sure that your grid certificate is active when running the commands.**

**Currently, the production is set to produce stop samples, this can be changed by editing the following parameters:**
in driver.py:
- dirgridpacks
- fnamegridpack_t
- fnamegridpack
- thiswdir
- fragmentfile_t

in submit.py:
- drivers_t
- fragmentfile_t

Before submitting the job with the submit.py script one should create the drivers with the desired parameters like this:

```
python driver.py -m 1000 -l 985 -c 20 -n 5000
```

After that the job can be submitted using

```
python submit.py -m 1000 -l 985 -c 20 -n 5000
```

this will only work if the drivers for the mass configuration have been created previously.
The resulting AODSIM, MINIAODSIM and NANOAODSIM files wil be stored under their respective directory in the STORE location.
