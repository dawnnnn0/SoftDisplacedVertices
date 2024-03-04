# Usage:
# python getGenFilterInfo.py /users/alikaan.gueven/samplesNewSeedNoDuplicates/customMINIAODSIM data.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-100To200.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-200To400_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-200To400.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-400To600_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-400To600.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-600To800_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-600To800.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-800To1200_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-800To1200.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-1200To2500_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-1200To2500.yaml
# python getGenFilterInfo.py /eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-2500ToInf_MC_UL18_CustomMiniAODv1-1/ database_meta/ZJetsToNuNu_HT-2500ToInf.yaml


from DataFormats.FWLite import Lumis, Handle
import os
import fnmatch
import yaml
import SoftDisplacedVertices.Samples.Samples as s


def get_metadata(ss, sample_version):
    """
    Gets sum of event weights for each ROOT file in each subdirectory.
    Creates a metadata.yaml file.
    """
    yaml_dict = dict()
    
    for sp in ss:
      sample_dir = sp.getFileDirs(sample_version)

      yaml_dict[sp.name] = {'totalsumWeights': None,
                         'totalsumPassWeights': None,
                         'files': []}

      for root, dirnames, filenames in os.walk(sample_dir):
        filename_list = []
        sumPassWeights = []
        sumWeights = []

        for filename in fnmatch.filter(filenames, '*.root'):
            filename_list.append(filename)
            file_path = os.path.join(root, filename)
            lumis = Lumis(file_path)
            lumisumWeights = []
            lumisumPassWeights = []
            for lumi in lumis:
                handle = Handle("GenFilterInfo")
                lumi.getByLabel('genFilterEfficiencyProducer', handle)
                GenFilterInfo = handle.product()
                lumisumWeights.append(GenFilterInfo.sumWeights())
                lumisumPassWeights.append(GenFilterInfo.sumPassWeights())
            
            sumWeights.append(sum(lumisumWeights))
            sumPassWeights.append(sum(lumisumPassWeights))

            yaml_dict[sp.name]['files'].append({'filename': filename,
                                             'sumWeights': sum(lumisumWeights),
                                             'sumPassWeights': sum(lumisumPassWeights)})

        
        totalsumWeights = sum(sumWeights)
        totalsumPassWeights = sum(sumPassWeights)

        yaml_dict[sp.name]['totalsumWeights'] = totalsumWeights
        yaml_dict[sp.name]['totalsumPassWeights'] = totalsumPassWeights

      if not yaml_dict[sp.name]['files']:
          yaml_dict.pop(sp.name)


    with open('metadata_'+sample_version+'.yaml', 'w') as outfile:
        yaml.safe_dump(yaml_dict, outfile, default_flow_style=False)
        

def get_metadata_dir(directory, outFileName):
    """
    Gets sum of event weights for each ROOT file in each subdirectory.
    Creates a metadata.yaml file.
    """
    yaml_dict = dict()
    
    for root, dirnames, filenames in os.walk(directory):
        filename_list = []
        sumPassWeights = []
        sumWeights = []
        yaml_dict[root] = {'totalsumWeights': None,
                           'totalsumPassWeights': None,
                           'files': []}

        
        for filename in fnmatch.filter(filenames, '*.root'):
            print(filename)
            filename_list.append(filename)
            file_path = os.path.join(root, filename)
            lumis = Lumis(file_path)
            lumisumWeights = []
            lumisumPassWeights = []
            for lumi in lumis:
                handle = Handle("GenFilterInfo")
                lumi.getByLabel('genFilterEfficiencyProducer', handle)
                GenFilterInfo = handle.product()
                lumisumWeights.append(GenFilterInfo.sumWeights())
                lumisumPassWeights.append(GenFilterInfo.sumPassWeights())
            
            sumWeights.append(sum(lumisumWeights))
            sumPassWeights.append(sum(lumisumPassWeights))

            yaml_dict[root]['files'].append({'filename': filename,
                                             'sumWeights': sum(lumisumWeights),
                                             'sumPassWeights': sum(lumisumPassWeights)})

        
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
    parser.add_argument('sample_version')
    parser.add_argument('outDir')
    args = parser.parse_args()
    input_samples = s.stop_2018
    s.loadData(input_samples,os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Samples/json/CustomMiniAOD_v3.json'),args.sample_version)
    get_metadata(input_samples,args.sample_version)
    #for sp in input_samples:
    #  sample_dir = sp.getFileDirs(args.sample_version)
    #  get_metadata(sample_dir, args.outDir+'/{}_{}.yaml'.format(args.sample_version,sp.name))
