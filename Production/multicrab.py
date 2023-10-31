#!/usr/bin/env python

import os
import sys

import yaml
import click
import CRABClient
from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

WORK_AREA = '/groups/hephy/cms/%s/sdv_prod' % os.getlogin()

def flatten(datasets):
    for key, value in datasets.iteritems():
        if isinstance(value, dict):
            for key1, value1 in flatten(value):
                yield key1, value1
        else:
            yield key, value
            
                
@click.group()
def cli():
    pass
   

@cli.command()
@click.option("--datasets", type=click.Path(exists=True, dir_okay=False), required=True) 
def submit(datasets):

    with open(datasets, "r") as inp:
        datasets_info = yaml.safe_load(inp)

    cfg = config()

    cfg.General.workArea = WORK_AREA
    cfg.General.transferOutputs = True

    cfg.JobType.pluginName = 'Analysis'
    cfg.JobType.maxMemoryMB = 4000

    cfg.Data.inputDBS = 'global'
    cfg.Data.splitting = 'Automatic'
    cfg.Data.publication = True
    
#    cfg.Site.blacklist=["T2_US_Florida", "T2_US_Vanderbilt"]

    cfg.Site.storageSite = 'T2_AT_Vienna'
    
    for dset_info in datasets_info:
        if os.environ['CMSSW_VERSION'] != dset_info['CMSSW']:
            print("fatal CMSSW")
            sys.exit()
            
        config_file = os.path.join(os.environ['CMSSW_BASE'], 'src', dset_info['config'])
        if not os.path.exists(config_file):
            print("Fatal configfile")
            sys.exit()
        cfg.JobType.psetName = config_file

        for key, value in flatten(dset_info['datasets']):

            job_dir = "{}/crab_{}_{}".format(WORK_AREA, key, dset_info['name'])
            if os.path.exists(job_dir):
                continue
            
            cfg.General.requestName = "{}_{}".format(key, dset_info['name'])
            cfg.Data.inputDataset = value
            cfg.Data.outputDatasetTag = "{}_{}".format(key, dset_info['name'])
            
            crabCommand('submit', config = cfg)
    
@cli.command()
@click.pass_obj
def status(datasets):
    with open('status.log', "w") as status_log:
        for request in os.listdir(WORK_AREA):
            job_dir = os.path.join(WORK_AREA, request)
            sys.stdout = status_log
            status = crabCommand("status", dir=job_dir)
            sys.stdout = sys.__stdout__ 
            print("{}: {}-{}".format(request[5:], status['dbStatus'], status['status']))
    

if __name__ == "__main__":
    cli()
