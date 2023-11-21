# Usage:
# python getGenFilterInfo.py /users/alikaan.gueven/samplesNewSeedNoDuplicates/customMINIAODSIM data.yaml

from DataFormats.FWLite import Lumis, Handle
import os
import fnmatch
import yaml



def get_metadata(directory, outFileName):
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
        yaml_dict[root] = {'totalsumWeights': None,
                           'totalsumPassWeights': None,
                           'files': []}

        
        for filename in fnmatch.filter(filenames, '*.root'):
            print(filename)
            filename_list.append(filename)
            file_path = os.path.join(root, filename)
            lumis = Lumis(file_path)
            handle = Handle("GenFilterInfo")
            lumis.getByLabel('genFilterEfficiencyProducer', handle)
            GenFilterInfo = handle.product()
            
            sumWeights.append(GenFilterInfo.sumWeights())
            sumPassWeights.append(GenFilterInfo.sumPassWeights())

            yaml_dict[root]['files'].append({'filename': filename,
                                             'sumWeights': GenFilterInfo.sumWeights(),
                                             'sumPassWeights': GenFilterInfo.sumPassWeights()})

        
        totalsumWeights = sum(sumWeights)
        totalsumPassWeights = sum(sumPassWeights)

        yaml_dict[root]['totalsumWeights'] = totalsumWeights
        yaml_dict[root]['totalsumPassWeights'] = totalsumPassWeights

        if not yaml_dict[root]['files']:
            yaml_dict.pop(root)


    with open(outFileName, 'w') as outfile:
        yaml.safe_dump(yaml_dict, outfile, default_flow_style=False)
        


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get GenFilterInfo metadata.')
    parser.add_argument('MINIAODSIM_dir')
    parser.add_argument('outFile')
    args = parser.parse_args()
    get_metadata(args.MINIAODSIM_dir, args.outFile)







