import time
import glob
import random

import torch
import torch.nn as nn

import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

import uproot
import ParT
import MTUprootDataLoader



print('CPU count: ', torch.multiprocessing.cpu_count())
# torch.set_num_threads(50)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


model = ParT.ParticleTransformer(5,
                                 2,
                                 pair_input_dim=0,
                                 embed_dims=[32, 128, 32],
                                 for_inference=True).to(device, dtype=float)
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

print(model)



ModifiedUprootIterator = MTUprootDataLoader.ModifiedUprootIterator



MLDATADIR = '/scratch-cbe/users/alikaan.gueven/ML_KAAN'
tmpList = glob.glob(f'{MLDATADIR}/predict/stop_M1000_988_ct200_2018/**/*.root', recursive=True)
tmpList = [file + ':Events' for file in tmpList]
trainList = tmpList[:10]
testList = tmpList[10:]

branchList = ['SDVSecVtx_Lxy', 'SDVSecVtx_LxySig', 'SDVSecVtx_pAngle', 'SDVSecVtx_charge', 'SDVSecVtx_ndof', 'SDVSecVtx_matchedLLPnDau_bydau']


shuffle = True
nWorkers = 4
step_size = 256

trainDataset = ModifiedUprootIterator(trainList, branchList, shuffle=shuffle, nWorkers=nWorkers, step_size=step_size)
trainLoader = torch.utils.data.DataLoader(trainDataset, num_workers=nWorkers, prefetch_factor=1, persistent_workers= True)

testDataset = ModifiedUprootIterator(testList, branchList, shuffle=shuffle, nWorkers=nWorkers, step_size=step_size)
testLoader = torch.utils.data.DataLoader(testDataset, num_workers=nWorkers, prefetch_factor=1, persistent_workers= True)


# -------------------------------- TRAINING ------------------------------------

epochs = 15

model.train()
for epoch in range(epochs):
    start_time = time.time()
    losses = []
    
    for batch_num, input_data in enumerate(trainLoader):
        optimizer.zero_grad()
        x, y = input_data
        x = x.to(device, dtype=float)
        y = y.to(device, dtype=float)

        x = x[0]

        ymaxSig = torch.max(y[0] > 1, axis=-1).values
        ymaxSig = ymaxSig.float()
        yBkg = (ymaxSig != 1).float()
        y = torch.concatenate((yBkg, ymaxSig), axis=-1)
        
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        losses.append(loss.item())

        optimizer.step()

        if batch_num % 4 == 0:
            pass
            # print('\tEpoch %d | Batch %d | Loss %6.2f' % (epoch, batch_num, loss.item()))
    if len(losses) > 0:
        print('Epoch %d | Loss %6.2f' % (epoch, sum(losses)/len(losses)))
    else:
        print('Epoch %d ' % (epoch))
    end_time = time.time()
    print(f"Time spent for epoch: {end_time - start_time:.2f}")




# -------------------------------- INFERENCE ------------------------------------

model.eval()

correct_predictions = []
all_predictions = []

# Inference on Test

with torch.no_grad():
    for (x,y) in testLoader:
        
        x = x.to(device, dtype=float)
        y = y.to(device, dtype=float)

        x = x[0]

        ymaxSig = torch.max(y[0] > 1, axis=-1).values
        ymaxSig = ymaxSig.float()
        yBkg = (ymaxSig != 1).float()
        y = torch.concatenate((yBkg, ymaxSig), axis=-1)
        
        pred = model(x).argmax(dim=-1)
        summ = np.sum(np.asarray(pred == y.argmax(dim=-1), dtype=float))
        size = pred.shape.numel()
        print(f'Batch accuracy after training: {summ/size:.3f}')



# Inference on Train

model.eval()

with torch.no_grad():
    for (x,y) in trainLoader:
        
        x = x.to(device, dtype=float)
        y = y.to(device, dtype=float)

        x = x[0]

        ymaxSig = torch.max(y[0] > 1, axis=-1).values
        ymaxSig = ymaxSig.float()
        yBkg = (ymaxSig != 1).float()
        y = torch.concatenate((yBkg, ymaxSig), axis=-1)
        
        pred = model(x).argmax(dim=-1)
        summ = np.sum(np.asarray(pred == y.argmax(dim=-1), dtype=float))
        size = pred.shape.numel()
        print(f'Batch accuracy after training: {summ/size:.3f}')









