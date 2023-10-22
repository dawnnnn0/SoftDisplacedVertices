Guide to using SampleGeneration

**IMPORTANT:** Change directories in the following locations:
- in submit.py the variable wdir should be set to the location where you want to run all jobs (logfiles will be saved there)
- in /templates/job_template.sh the variable STORE should be set to the location where you want to store the resulting .root files

There are two python scripts which are used to operate the signal generation process:
- driver.py
- submit.py

The driver.py file is a wrapper to create the config files needed for cmsRun, while the role of
submit.py is to submit the job file that executes all the cmsRun commands. There are multiple parameters that can be used:
(- stopmass (s): mass of the stop, default is 600, this has now been replaced by n2n3mass for our generation purposes)
- n2n3mass (m): mass of n2n3, default is 600
- lspmass (l): mass of the lsp, default is 588
- ctau (c): lifetime of the stop, default is 200
- nevents (n): number of simulated events, default is 5000

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