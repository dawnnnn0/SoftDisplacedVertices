# This is a class that include necessary information of a sample.
import os

class Sample:
  def __init__(self, name, xsec, filter_eff=1):
    self.name = name
    self.xsec = xsec
    self.filter_eff = filter_eff
    self.dirs = {}
    self.dataset = {}
    self.dataset_instance = {}


  def setDirs(self, label, dirs):
    assert label not in self.dirs
    self.dirs[label] = dirs

  def setDataset(self, label, dataset, instance):
    assert label not in self.dataset
    assert label not in self.dataset_instance
    self.dataset[label] = dataset
    self.dataset_instance[label] = instance

  def getFileList(self, label, namebase):
    #FIXME: Make this work for DBS
    assert label in self.dirs
    fileNames = []
    for root, dirs, files in os.walk(self.dirs[label]):
      for ifile in files:
        if (namebase in ifile and ifile.endswith('.root')):
          fileNames.append(os.path.join(root,ifile))

    return fileNames

  def getFileDirs(self,label):
    return self.dirs[label]

  def getNEvents(self):
    return -1

  # Make sure getNEvents are getting the number of events in the full dataset before using this method. Otherwise it will be very wrong
  #def getLumiWeights(self, lumi):
  #  if self.getNEvents()==-1:
  #    print("WARNING! Number of events are not available!")
  #    return 1
  #  return lumi*self.xsec/self.getNEvents()
