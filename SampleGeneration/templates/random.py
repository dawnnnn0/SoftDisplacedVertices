from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper

def random(process):
    RandomNumberServiceHelper(process.RandomNumberGeneratorService).populate()

    return process
