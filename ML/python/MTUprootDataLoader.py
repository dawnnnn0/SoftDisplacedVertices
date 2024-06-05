import random

import torch
import numpy as np
import awkward as ak

import uproot

class ModifiedUprootIterator(torch.utils.data.IterableDataset):
    def __init__(self, files, branches, shuffle=True, nWorkers=1, step_size=1024):
        """
        Parameters
        ----------
        files : list
                list of files with the TTree (e.g. ['path_to_file:Events', ...])
        branches : list
                list of branches in TTree. Last branch implies the labels to the classifier.
        nWorkers : int
                Files will be divided among the workers.
                Therefore, nWorkers determines number of divisions.
                nWorkers=0 will be treated as nWorkers=1.
        step_size : int
                number of Events to be read from the files at each iteration.
        """
        
        print('Initialize iterable dataset')
        self.files = files
        self.branches = branches
        self.step_size = step_size
        self.nWorkers = nWorkers
        
        if shuffle:
            random.shuffle(self.files)

        if nWorkers == 0: nWorkers=1 # Min nWorkers should be great
        self.workerTrainList = [[self.files[i] for i in range(len(self.files)) if i % nWorkers == worker_info_id] for worker_info_id in range(nWorkers)]
        self.iteratorList = [uproot.iterate(workerXInput, self.branches, step_size=self.step_size) for workerXInput in self.workerTrainList]
        self.x = None
        

    def __iter__(self):
        """
        Refresh all the iterators in the iteratorList.
        Will be run at the end of each epoch.
        """
        self.iteratorList = [uproot.iterate(workerXInput, self.branches, step_size=self.step_size) for workerXInput in self.workerTrainList]
        return self

    
    def __next__(self):
        """
        next method to get the inputs to the network.

        Note to myself (KAAN): Maybe I can separate some part of the code into the preprocessing step.
                               But remember that DataLoader always return torch tensors or numpy arrays etc.
        """
        worker_info = torch.utils.data.get_worker_info()
        if worker_info:
            x = next(self.iteratorList[worker_info.id])
        elif not worker_info and self.nWorkers < 2: # Single threaded
            x = next(self.iteratorList[0])
        else:
            x = next(self.iteratorList[0])

        
        features = x.fields[:]
        features.remove('SDVSecVtx_matchedLLPnDau_bydau')
        
        X = []
        for feature in features:
            flat_vtx_feat = ak.flatten(x[feature], axis=None)
            X.append(flat_vtx_feat[..., np.newaxis])
        
        features_tensor = torch.tensor(ak.concatenate(X, axis=-1))

        y = ak.flatten(x['SDVSecVtx_matchedLLPnDau_bydau'])[..., np.newaxis]
        y_0 = y<2
        y_1 = y>=2
        label_tensor = torch.tensor(ak.concatenate([y_0, y_1], axis=-1), dtype=float)

        return features_tensor, label_tensor