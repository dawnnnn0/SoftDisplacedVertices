import os, sys, glob
import getopt, datetime
import shutil

##################################################
##### FUNCTION DEFINITIONS FOR EVENT NUMBER ######
##################################################

def save_value_to_file(value):
    with open("config.txt", "w") as file:
        file.write(str(value))

def read_value_from_file():
    try:
        with open("config.txt", "r") as file:
            return int(file.read().strip())
    except IOError:
        save_value_to_file(1)
        return 1

##################################################

########## setup

home = os.getcwd()
dirtemplates = home + "/templates"
dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2"
fnamegridpack_t = "SMS-C1N2_mC1-C1N2MASS_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
#dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-StopStop/v1"
#fnamegridpack_t = "SMS-StopStop_mStop-STOPMASS_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz"
#dirgridpacks = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-N2N3/v1"
#fnamegridpack_t = "SMS-N2N3_mN-N2N3MASS_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz"
dirdrivers = home + "/drivers"
#wdir = home + "/simulations"
wdir = "/scratch/felix.lang/SignalProduction/simulations"

########## options

opts, args = getopt.getopt(sys.argv[1:], "rdm:l:c:n:", ["reset", "dryrun", "llpmass=", "lspmass=", "ctau=", "nevents="])

reset = False
dryrun = False
llpmass = 600.
lspmass = 588.
ctau = 200.  # in mm!
nevents = 5000

for opt, arg in opts:
    if opt in ("-r", "--reset"):
        reset = True
    if opt in ("-d", "--dryrun"):
        dryrun = True
    if opt in ("-m", "--llpmass"):
        llpmass = float(arg)
    if opt in ("-l", "--lspmass"):
        lspmass = float(arg)
    if opt in ("-c", "--ctau"):
        ctau = float(arg)
    if opt in ("-n", "--nevents"):
        nevents = int(arg)

if reset:
    save_value_to_file(1)
firstEvent = read_value_from_file()
save_value_to_file(firstEvent + nevents)


fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("C1N2MASS", str(int(llpmass)))
#fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("STOPMASS", str(int(stopmass)))
#fnamegridpack = dirgridpacks + "/" + fnamegridpack_t.replace("N2N3MASS", str(int(n2n3mass)))
drivers_t = dirdrivers + "/C1N2_{}_{}_{}_{}".format(llpmass, lspmass, ctau, nevents)
#drivers_t = dirdrivers + "/STOP_{}_{}_{}_{}".format(stopmass, lspmass, ctau, nevents)
#drivers_t = dirdrivers + "/N2N3_{}_{}_{}_{}".format(n2n3mass, lspmass, ctau, nevents)

if not os.path.exists(fnamegridpack):
    exit("gridpack " + fnamegridpack + " does not exists; change the llp mass")
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

'''
if rewrite and lastndir:
    thiswdir = "run{}".format(lastndir)
    os.system("rm -rf " + thiswdir)
else:
    thiswdir = "run{}".format(lastndir + 1)
'''

thiswdir = "run{}".format(lastndir + 1)

os.mkdir(thiswdir)
os.chdir(thiswdir)
os.environ["RUN_NUMBER"] = thiswdir
os.environ["FIRST_EVENT"] = str(firstEvent)

jobfile_t = dirtemplates + "/job_template.sh"
jobfile = "job.sh"

fragmentfile_t = dirtemplates + "/SMS_C1N2-fragment_template.py"
#fragmentfile_t = dirtemplates + "/STOP-fragment_template.py"
#fragmentfile_t = dirtemplates + "/SMS_N2N3-fragment_template.py"
fragmentfile = "fragment.py"

random_t = dirtemplates + "/random.py"
random = "random.py"

drivers = "drivers"

shutil.copyfile(random_t, random)

shutil.copyfile(fragmentfile_t, fragmentfile)
os.system('sed -i "s|C1N2MASS|' + str(llpmass) + '|g" ' + fragmentfile)
#os.system('sed -i "s|STOPMASS|' + str(stopmass) + '|g" ' + fragmentfile)
#os.system('sed -i "s|N2N3MASS|' + str(n2n3mass) + '|g" ' + fragmentfile)
os.system('sed -i "s|LSPMASS|' + str(lspmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|CTAUVALUE|' + str(ctau) + '|g" ' + fragmentfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + fragmentfile)
os.system('sed -i "s|GRIDPACKFILE|' + str(fnamegridpack) + '|g" ' + fragmentfile)

shutil.copyfile(jobfile_t, jobfile)
os.system('sed -i "s|PROCESS|' + "C1N2" + '|g" ' + jobfile)
#os.system('sed -i "s|PROCESS|' + "STOP" + '|g" ' + jobfile)
#os.system('sed -i "s|PROCESS|' + "N2N3" + '|g" ' + jobfile)
os.system('sed -i "s|LLPMASS|' + str(int(llpmass)) + '|g" ' + jobfile)
os.system('sed -i "s|LSPMASS|' + str(int(lspmass)) + '|g" ' + jobfile)
os.system('sed -i "s|CTAUVALUE|' + str(int(ctau)) + '|g" ' + jobfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + jobfile)

shutil.copytree(drivers_t, drivers)

########## submit jobs

if not dryrun:
    os.system("sbatch job.sh")

#os.system("bash job.sh")