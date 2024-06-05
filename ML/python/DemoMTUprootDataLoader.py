import time
import glob
import random

import torch
import torch.nn as nn
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

import uproot
import ROOT

import MTUprootDataLoader

print('CPU count: ', torch.multiprocessing.cpu_count())

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.linear1 = nn.Linear(5, 200)
        self.linear2 = nn.Linear(200, 500)
        self.linear3 = nn.Linear(500, 2)
        self.softmax = nn.Softmax(-1)
    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        x = self.linear3(x)
        out = self.softmax(x)
        return out

model = MLP().to(device)
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

print(model)


ModifiedUprootIterator = MTUprootDataLoader.ModifiedUprootIterator


MLDATADIR = '/scratch-cbe/users/alikaan.gueven/ML_KAAN'
tmpList = glob.glob(f'{MLDATADIR}/predict/stop_M1000_988_ct200_2018/**/*.root', recursive=True)
tmpList = [file + ':Events' for file in tmpList]
trainList = tmpList[:10]
testList = tmpList[10:]

branchList = ['SDVSecVtx_Lxy', 'SDVSecVtx_x', 'SDVSecVtx_y', 'SDVSecVtx_z', 'SDVSecVtx_ndof', 'SDVSecVtx_matchedLLPnDau_bydau']


shuffle = True
nWorkers = 5
step_size = 1024

trainDataset = ModifiedUprootIterator(tmpList, branchList, shuffle=shuffle, nWorkers=nWorkers, step_size=step_size)
trainLoader = torch.utils.data.DataLoader(trainDataset, num_workers=nWorkers, prefetch_factor=1, persistent_workers= True)

testDataset = ModifiedUprootIterator(testList, branchList, shuffle=shuffle, nWorkers=nWorkers, step_size=step_size)
testLoader = torch.utils.data.DataLoader(testDataset, num_workers=nWorkers, prefetch_factor=1, persistent_workers= True)


epochs = 5

model.train()
for epoch in range(epochs):
    start_time = time.time()
    losses = []
    
    for batch_num, input_data in enumerate(trainLoader):
        optimizer.zero_grad()
        x, y = input_data
        x = x.to(device).float()
        y = y.to(device)
        
        output = model(x[0])
        loss = criterion(output, y[0])
        loss.backward()
        losses.append(loss.item())

        optimizer.step()

        if batch_num % 40 == 0:
            print('\tEpoch %d | Batch %d | Loss %6.2f' % (epoch, batch_num, loss.item()))
    if len(losses) > 0:
        print('Epoch %d | Loss %6.2f' % (epoch, sum(losses)/len(losses)))
    else:
        print('Epoch %d ' % (epoch))
    end_time = time.time()
    print("Time spent for epoch: ", end_time - start_time)



model.eval()

with torch.no_grad():
    for (x,y) in testLoader:
        x = x[0].to(device).float()
        pred = model(x).argmax(dim=-1)
        summ = np.sum(np.asarray(pred == y.argmax(dim=-1), dtype=float))
        size = pred.shape.numel()
        print(f'Batch accuracy after training: {summ/size:.3f}')









