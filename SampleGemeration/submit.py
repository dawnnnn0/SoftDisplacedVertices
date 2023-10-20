import os, sys, glob
import getopt, datetime
import shutil

########## setup

home = os.getcwd()
dirtemplates = home + "/templates"
dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-StopStop/v1"
fnamegridpack_t = "SMS-StopStop_mStop-STOPMASS_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz"
wdir = "/scratch/felix.lang/SignalProduction/simulations"

########## options

opts, args = getopt.getopt(sys.argv[1:], "rds:l:c:", ["rewrite", "dryrun", "stopmass=", "lspmass=", "ctau="])

rewrite = False
dryrun = False
stopmass = 600.
lspmass = 588.
ctau = 200.  # in mm!

for opt, arg in opts:
    if opt in ("-r", "--rewrite"):
        rewrite = True
    if opt in ("-d", "--dryrun"):
        dryrun = True
    if opt in ("-s", "--stopmass"):
        stopmass = float(arg)
    if opt in ("-l", "--lspmass"):
        lspmass = float(arg)
    if opt in ("-c", "--ctau"):
        ctau = float(arg)

fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("STOPMASS", str(int(stopmass)))

if not os.path.exists(fnamegridpack):
    exit("gridpack " + fnamegridpack + " does not exists; change the stop mass")

########## prepare working directory

os.chdir(wdir)

wdirs = glob.glob("run*")

ndirs = [0]
for wdir in wdirs:
    ndirs.append(int(wdir[3:]))
lastndir = max(ndirs)

if rewrite and lastndir:
    thiswdir = "run{}".format(lastndir)
    os.system("rm -rf " + thiswdir)
else:
    thiswdir = "run{}".format(lastndir + 1)

os.mkdir(thiswdir)
os.chdir(thiswdir)

jobfile_t = dirtemplates + "/job_template.sh"
jobfile = "job.sh"

fragmentfile_t = dirtemplates + "/test-fragment_template.py"
fragmentfile = "test-fragment.py"

templates_t = home + "/drivers"
templates = "drivers"

shutil.copyfile(jobfile_t, jobfile)
os.system('sed -i "s|STOPMASS|' + str(int(stopmass)) + '|g" ' + jobfile)
os.system('sed -i "s|LSPMASS|' + str(int(lspmass)) + '|g" ' + jobfile)
os.system('sed -i "s|CTAUVALUE|' + str(int(ctau)) + '|g" ' + jobfile)

shutil.copyfile(fragmentfile_t, fragmentfile)
os.system('sed -i "s|STOPMASS|' + str(stopmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|LSPMASS|' + str(lspmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|CTAUVALUE|' + str(ctau) + '|g" ' + fragmentfile)
os.system('sed -i "s|GRIDPACKFILE|' + str(fnamegridpack) + '|g" ' + fragmentfile)

shutil.copytree(templates_t, templates)

########## submit jobs

if not dryrun:
    os.system("sbatch job.sh")