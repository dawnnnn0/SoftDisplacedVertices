# Usage:
# python printGenFilterInfo.py /users/alikaan.gueven/samplesNewSeedNoDuplicates/customMINIAODSIM

from DataFormats.FWLite import Lumis, Handle
import os
import fnmatch
import yaml



def get_metadata(directory):
    """
    Gets sum of event weights for each ROOT file in each subdirectory.
    Creates a metadata.yaml file.
    """
    yaml_dict = dict()
    
    for root, dirnames, filenames in os.walk(directory):
        filename_list = []
        sumPassWeights = []
        sumPassWeights2 = []
        sumWeights = []
        sumWeights2 = []
        for filename in fnmatch.filter(filenames, '*.root'):
            print(filename)
            filename_list.append(filename)
            file_path = os.path.join(root, filename)
            lumis = Lumis(file_path)
            for lumi in lumis:
                handle = Handle("GenFilterInfo")
                lumis.getByLabel('genFilterEfficiencyProducer', handle)
                GenFilterInfo = handle.product()
            
                sumWeights.append(GenFilterInfo.sumWeights())
                sumPassWeights.append(GenFilterInfo.sumPassWeights())
            print(sumWeights)
        


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get GenFilterInfo metadata.')
    parser.add_argument('MINIAODSIM_dir')
    args = parser.parse_args()
    get_metadata(args.MINIAODSIM_dir)







