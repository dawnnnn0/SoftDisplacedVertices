import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

#Need hbar*c to convert lifetime to width
hBarCinGeVmm = 1.973269788e-13

mC1N2 = C1N2MASS
mLSP = LSPMASS
CTAU = CTAUVALUE

WCHI2 = hBarCinGeVmm/CTAU

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring("GRIDPACKFILE"),
    nEvents = cms.untracked.uint32(EVENTCOUNT),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

SLHA_TABLE="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     %MC1N2%          # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     %MC1N2%          # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+
   1000039     1.00000000E+05   # ~gravitino

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     %WCHI2%   # neutralino2 decays
    0.00000000E+00    3     1000022   5   -5  # Dummy decay
    0.50000000E+00    2     1000022   25      # BR(N2 -> N1 + H)
    0.500000000E+00   2     1000022   23      # BR(N2 -> N1 + Z)
DECAY   1000024     1.00000000E-01   # chargino1+ decays
    0.00000000E+00    3     1000022   5   -5  # Dummy decay 
    1.00000000E+00    2     1000022   24      # BR(N3 -> N1 + W)
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
""".replace('%MLSP%','%e' % mLSP).replace('%MC1N2%','%e' % mC1N2).replace('%WCHI2%','%e' % WCHI2)

import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    SLHATableForPythia8 = cms.string('%s' % SLHA_TABLE),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP2SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            '1000023:tau0 = %.1f' % CTAU,
            'LesHouches:setLifetime = 2',
        ),
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 76.', #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '6:m0 = 172.5',
#            '25:onMode = off',
#            '25:onIfMatch = 5 -5', # Only H->bb decays
            '25:m0 = 125.0',
#            '23:onMode = off',
#            '23:onIfAny = 1 2 3 4 5', # Only Z->qq decays
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP2Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    'JetMatchingParameters',
                                    )
    )
)

#ProductionFilterSequence = cms.Sequence(generator)

#     Filter setup
# ------------------------
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/PhysicsTools/HepMCCandAlgos/python/genParticles_cfi.py
tmpGenParticles = cms.EDProducer("GenParticleProducer",
saveBarCodes = cms.untracked.bool(True),
src = cms.InputTag("generator","unsmeared"),
abortOnUnknownPDGCode = cms.untracked.bool(False)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/Configuration/python/GenJetParticles_cff.py
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoMET/Configuration/python/GenMETParticles_cff.py
tmpGenParticlesForJetsNoNu = cms.EDProducer("InputGenJetsParticleSelector",
src = cms.InputTag("tmpGenParticles"),
ignoreParticleIDs = cms.vuint32(
     1000022,
     1000012, 1000014, 1000016,
     2000012, 2000014, 2000016,
     1000039, 5100039,
     4000012, 4000014, 4000016,
     9900012, 9900014, 9900016,
     39,12,14,16),
partonicFinalState = cms.bool(False),
excludeResonances = cms.bool(False),
excludeFromResonancePids = cms.vuint32(12, 13, 14, 16),
tausAsJets = cms.bool(False)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/AnomalousCellParameters_cfi.py
AnomalousCellParameters = cms.PSet(
maxBadEcalCells         = cms.uint32(9999999),
maxRecoveredEcalCells   = cms.uint32(9999999),
maxProblematicEcalCells = cms.uint32(9999999),
maxBadHcalCells         = cms.uint32(9999999),
maxRecoveredHcalCells   = cms.uint32(9999999),
maxProblematicHcalCells = cms.uint32(9999999)
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/GenJetParameters_cfi.py
GenJetParameters = cms.PSet(
src            = cms.InputTag("tmpGenParticlesForJetsNoNu"),
srcPVs         = cms.InputTag(''),
jetType        = cms.string('GenJet'),
jetPtMin       = cms.double(3.0),
inputEtMin     = cms.double(0.0),
inputEMin      = cms.double(0.0),
doPVCorrection = cms.bool(False),
# pileup with offset correction
doPUOffsetCorr = cms.bool(False),
   # if pileup is false, these are not read:
   nSigmaPU = cms.double(1.0),
   radiusPU = cms.double(0.5),
# fastjet-style pileup
doAreaFastjet  = cms.bool(False),
doRhoFastjet   = cms.bool(False),
  # if doPU is false, these are not read:
  Active_Area_Repeats = cms.int32(5),
  GhostArea = cms.double(0.01),
  Ghost_EtaMax = cms.double(6.0),
Rho_EtaMax = cms.double(4.5),
useDeterministicSeed= cms.bool( True ),
minSeed             = cms.uint32( 14327 )
)

# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoJets/JetProducers/python/ak4GenJets_cfi.py
tmpAk4GenJetsNoNu = cms.EDProducer(
"FastjetJetProducer",
GenJetParameters,
AnomalousCellParameters,
jetAlgorithm = cms.string("AntiKt"),
rParam       = cms.double(0.4)
)

genHTFilter = cms.EDFilter("GenHTFilter",
src = cms.InputTag("tmpAk4GenJetsNoNu"), #GenJet collection as input
jetPtCut = cms.double(30.0), #GenJet pT cut for HT
jetEtaCut = cms.double(5.0), #GenJet eta cut for HT
genHTcut = cms.double(200.0) #genHT cut
)

tmpGenMetTrue = cms.EDProducer("GenMETProducer",
src = cms.InputTag("tmpGenParticlesForJetsNoNu"),
onlyFiducialParticles = cms.bool(False), ## Use only fiducial GenParticles
globalThreshold = cms.double(0.0), ## Global Threshold for input objects
usePt   = cms.bool(True), ## using Pt instead Et
applyFiducialThresholdForFractions   = cms.bool(False),
)

genMETfilter1 = cms.EDFilter("CandViewSelector",
 src = cms.InputTag("tmpGenMetTrue"),
 cut = cms.string("pt > 100")
)

genMETfilter2 = cms.EDFilter("CandViewCountFilter",
src = cms.InputTag("genMETfilter1"),
minNumber = cms.uint32(1),
)

ProductionFilterSequence = cms.Sequence(generator*
                                    tmpGenParticles * tmpGenParticlesForJetsNoNu *
                                    tmpAk4GenJetsNoNu * genHTFilter *
                                    tmpGenMetTrue * genMETfilter1 * genMETfilter2
)
