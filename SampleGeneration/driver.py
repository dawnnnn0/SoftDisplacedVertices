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
wdir = home + "/drivers"

########## options

### USED FOR STOP ###
'''
opts, args = getopt.getopt(sys.argv[1:], "s:l:c:n:", ["stopmass=", "lspmass=", "ctau=", "nevents="])

stopmass = 600.
lspmass = 588.
ctau = 200.  # in mm!
nevents = 5000

for opt, arg in opts:
    if opt in ("-s", "--stopmass"):
        stopmass = float(arg)
    if opt in ("-l", "--lspmass"):
        lspmass = float(arg)
    if opt in ("-c", "--ctau"):
        ctau = float(arg)
    if opt in ("-n", "--nevents"):
        nevents = int(arg)
'''

opts, args = getopt.getopt(sys.argv[1:], "m:l:c:n:", ["n2n3mass=", "lspmass=", "ctau=", "nevents="])

n2n3mass = 600.
lspmass = 588.
ctau = 200.  # in mm!
nevents = 5000

for opt, arg in opts:
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

if not os.path.exists(fnamegridpack):
    exit("gridpack " + fnamegridpack + " does not exists; change the mass")

########## prepare working directory

if not os.path.exists(wdir):
    os.mkdir(wdir)
os.chdir(wdir)

#thiswdir = "STOP{}_{}_{}_{}".format(stopmass, lspmass, ctau, nevents)
thiswdir = "N2N3_{}_{}_{}_{}".format(n2n3mass, lspmass, ctau, nevents)

if os.path.exists(thiswdir):
    shutil.rmtree(thiswdir)

os.mkdir(thiswdir)
os.chdir(thiswdir)

setupfile_t = dirtemplates + "/setup_template.sh"
setupfile = "setup.sh"

#fragmentfile_t = dirtemplates + "/STOP-fragment_template.py"
fragmentfile_t = dirtemplates + "/SMS_N2N3-fragment_template.py"
fragmentfile = "fragment.py"

random_t = dirtemplates + "/random.py"
random = "random.py"

shutil.copyfile(random_t, random)

shutil.copyfile(setupfile_t, setupfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + setupfile)

shutil.copyfile(fragmentfile_t, fragmentfile)
#os.system('sed -i "s|STOPMASS|' + str(stopmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|N2N3MASS|' + str(n2n3mass) + '|g" ' + fragmentfile)
os.system('sed -i "s|LSPMASS|' + str(lspmass) + '|g" ' + fragmentfile)
os.system('sed -i "s|CTAUVALUE|' + str(ctau) + '|g" ' + fragmentfile)
os.system('sed -i "s|EVENTCOUNT|' + str(nevents) + '|g" ' + fragmentfile)
os.system('sed -i "s|GRIDPACKFILE|' + str(fnamegridpack) + '|g" ' + fragmentfile)

########## submit jobs

#if not dryrun:
#    os.system("sbatch job.sh")

os.system("bash setup.sh")
