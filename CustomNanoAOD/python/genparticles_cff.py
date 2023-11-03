
# Comment:
# This is just kept for historical reasons.
# Not used in the main code.
# Could be discarded in the future.



import FWCore.ParameterSet.Config as cms

genParticleTableForSDV = cms.EDProducer("SimpleCandidateFlatTableProducer",
    cut = cms.string(''),
    doc = cms.string('interesting gen particles '),
    extension = cms.bool(False),
    name = cms.string('SDVGenPart'),
    singleton = cms.bool(False),
    src = cms.InputTag("finalGenParticlesWithStableCharged"),
    variables = cms.PSet(
        eta = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('eta'),
            expr = cms.string('eta'),
            mcOnly = cms.bool(False),
            precision = cms.int32(8),
            type = cms.string('float')
        ),
        genPartIdxMother = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('index of the mother particle'),
            expr = cms.string('?numberOfMothers>0?motherRef(0).key():-1'),
            mcOnly = cms.bool(False),
            precision = cms.int32(-1),
            type = cms.string('int')
        ),
        mass = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('Mass stored for all particles with the exception of quarks (except top), leptons/neutrinos, photons with mass < 1 GeV, gluons, pi0(111), pi+(211), D0(421), and D+(411). For these particles, you can lookup the value from PDG.'),
            expr = cms.string('?!((abs(pdgId)>=1 && abs(pdgId)<=5) || (abs(pdgId)>=11 && abs(pdgId)<=16) || pdgId==21 || pdgId==111 || abs(pdgId)==211 || abs(pdgId)==421 || abs(pdgId)==411 || (pdgId==22 && mass<1))?mass:0'),
            mcOnly = cms.bool(False),
            precision = cms.string('?(abs(pdgId)==6 && statusFlags().isLastCopy())?20:8'),
            type = cms.string('float')
        ),
        pdgId = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('PDG id'),
            expr = cms.string('pdgId'),
            mcOnly = cms.bool(False),
            precision = cms.int32(-1),
            type = cms.string('int')
        ),
        phi = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('phi'),
            expr = cms.string('phi'),
            mcOnly = cms.bool(False),
            precision = cms.int32(8),
            type = cms.string('float')
        ),
        pt = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('pt'),
            expr = cms.string('pt'),
            mcOnly = cms.bool(False),
            precision = cms.int32(8),
            type = cms.string('float')
        ),
        status = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('Particle status. 1=stable'),
            expr = cms.string('status'),
            mcOnly = cms.bool(False),
            precision = cms.int32(-1),
            type = cms.string('int')
        ),
        statusFlags = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('gen status flags stored bitwise, bits are: 0 : isPrompt, 1 : isDecayedLeptonHadron, 2 : isTauDecayProduct, 3 : isPromptTauDecayProduct, 4 : isDirectTauDecayProduct, 5 : isDirectPromptTauDecayProduct, 6 : isDirectHadronDecayProduct, 7 : isHardProcess, 8 : fromHardProcess, 9 : isHardProcessTauDecayProduct, 10 : isDirectHardProcessTauDecayProduct, 11 : fromHardProcessBeforeFSR, 12 : isFirstCopy, 13 : isLastCopy, 14 : isLastCopyBeforeFSR, '),
            expr = cms.string('statusFlags().isLastCopyBeforeFSR()                  * 16384 +statusFlags().isLastCopy()                           * 8192  +statusFlags().isFirstCopy()                          * 4096  +statusFlags().fromHardProcessBeforeFSR()             * 2048  +statusFlags().isDirectHardProcessTauDecayProduct()   * 1024  +statusFlags().isHardProcessTauDecayProduct()         * 512   +statusFlags().fromHardProcess()                      * 256   +statusFlags().isHardProcess()                        * 128   +statusFlags().isDirectHadronDecayProduct()           * 64    +statusFlags().isDirectPromptTauDecayProduct()        * 32    +statusFlags().isDirectTauDecayProduct()              * 16    +statusFlags().isPromptTauDecayProduct()              * 8     +statusFlags().isTauDecayProduct()                    * 4     +statusFlags().isDecayedLeptonHadron()                * 2     +statusFlags().isPrompt()                             * 1      '),
            mcOnly = cms.bool(False),
            precision = cms.int32(-1),
            type = cms.string('int')
        )
    )
)
