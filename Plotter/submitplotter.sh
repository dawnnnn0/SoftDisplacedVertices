set -e

### DATA
python3 autoplotter.py --sample met_2018 --output /eos/vbc/group/cms/ang.li/DataHistos_VRCR${1} --config configs/plotconfig_${2}.yaml --lumi -1 --json Data_production_20240326.json --datalabel CustomNanoAOD --data --year 2018 --nfiles 10 --submit
submit jobs.sh --nCPUs=4

### BKG MC
python3 autoplotter.py --sample stop_2018 znunu_2018 wlnu_2018 qcd_2018 top_2018 --output /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1} --config configs/plotconfig_${2}.yaml --lumi 59683. --json MC_RunIISummer20UL18.json --datalabel CustomNanoAOD --year 2018 --nfiles 10 --submit
submit jobs.sh --nCPUs=4

### SIG MC
#python3 autoplotter.py --sample stop_2018 --output /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}_sig --config configs/plotconfig_${2}sig.yaml --lumi 59683. --json MC_RunIISummer20UL18.json --datalabel CustomNanoAOD --year 2018 --submit
#submit jobs.sh --nCPUs=8

### FAILED JOBS
#python3 autoplotter.py --sample zjetstonunuht0400_2018 --output /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}_fix --config configs/plotconfig_${2}.yaml --lumi 59683. --json MC_RunIISummer20UL18.json --datalabel CustomNanoAOD --year 2018 --submit
#submit jobs.sh --nCPUs=8
