import os, sys, glob
import getopt, datetime
import shutil

########## setup

home = os.getcwd()
dirtemplates = home + "/templates"
#dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-StopStop/v1"
#fnamegridpack_t = "SMS-StopStop_mStop-STOPMASS_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz"
dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-N2N3/v1"
fnamegridpack_t = "SMS-N2N3_mN-N2N3MASS_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz"
dirdrivers = home + "/drivers"
#wdir = home + "/simulations"
wdir = "/scratch/felix.lang/SignalProduction/simulations"

########## options

### USED FOR STOP ###
'''
opts, args = getopt.getopt(sys.argv[1:], "rds:l:c:n:", ["rewrite", "dryrun", "stopmass=", "lspmass=", "ctau=", "nevents="])

rewrite = False
dryrun = False
stopmass = 600.
lspmass = 588.
ctau = 200.  # in mm!
nevents = 5000

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
    if opt in ("-n", "--nevents"):
        nevents = int(arg)
'''

opts, args = getopt.getopt(sys.argv[1:], "rdm:l:c:n:", ["rewrite", "dryrun", "n2n3mass=", "lspmass=", "ctau=", "nevents="])

rewrite = False
dryrun = False
n2n3mass = 600.
lspmass = 588.
ctau = 200.  # in mm!
nevents = 5000

for opt, arg in opts:
    if opt in ("-r", "--rewrite"):
        rewrite = True
    if opt in ("-d", "--dryrun"):
        dryrun = True
    if opt in ("-m", "--n2n3mass"):
        n2n3mass = float(arg)
    if opt in ("-l", "--lspmass"):
        lspmass = float(arg)
    if opt in ("-c", "--ctau"):
        ctau = float(arg)
    if opt in ("-n", "--nevents"):
        nevents = int(arg)

#fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("STOPMASS", str(int(stopmass)))
fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("N2N3MASS", str(int(n2n3mass)))
#drivers_t = dirdrivers + "/STOP_{}_{}_{}_{}".format(stopmass, lspmass, ctau, nevents)
drivers_t = dirdrivers + "/N2N3_{}_{}_{}_{}".format(n2n3mass, lspmass, ctau, nevents)

if not os.path.exists(fnamegridpack):
    exit("gridpack " + fnamegridpack + " does not exists; change the mass")
if not os.path.exists(drivers_t):
    exit("No existing drivers for mass configuration, create drivers first")

########## prepare working directory

if not os.path.exists(wdir):
    os.mkdir(wdir)
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
os.environ["RUN_NUMBER"] = thiswdir

jobfile_t = dirtemplates + "/job_template.sh"
jobfile = "job.sh"

#fragmentfile_t = dirtemplates + "/STOP-fragment_template.py"
fragmentfile_t = dirtemplates + "/SMS_N2N3-fragment_template.py"
fragmentfile = "fragment.py"

random_t = dirtemplates + "/random.py"
random = "random.py"

drivers = "drivers"

shutil.copyfile(random_t, random)

shutil.copyfile(fragmentfile_t, fragmentfile)
#os.system('sed -i "s|STOPMASS|' + str(stopmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|N2N3MASS|' + str(n2n3mass) + '|g" ' + fragmentfile)
os.system('sed -i "s|LSPMASS|' + str(lspmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|CTAUVALUE|' + str(ctau) + '|g" ' + fragmentfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + fragmentfile)
os.system('sed -i "s|GRIDPACKFILE|' + str(fnamegridpack) + '|g" ' + fragmentfile)

shutil.copyfile(jobfile_t, jobfile)
#os.system('sed -i "s|PROCESS|' + "STOP" + '|g" ' + jobfile)
os.system('sed -i "s|PROCESS|' + "N2N3" + '|g" ' + jobfile)
#os.system('sed -i "s|IMASS|' + str(int(stopmass)) + '|g" ' + jobfile)
os.system('sed -i "s|IMASS|' + str(int(n2n3mass)) + '|g" ' + jobfile)
os.system('sed -i "s|LSPMASS|' + str(int(lspmass)) + '|g" ' + jobfile)
os.system('sed -i "s|CTAUVALUE|' + str(int(ctau)) + '|g" ' + jobfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + jobfile)

shutil.copytree(drivers_t, drivers)

########## submit jobs

if not dryrun:
    os.system("sbatch job.sh")

#os.system("bash job.sh")