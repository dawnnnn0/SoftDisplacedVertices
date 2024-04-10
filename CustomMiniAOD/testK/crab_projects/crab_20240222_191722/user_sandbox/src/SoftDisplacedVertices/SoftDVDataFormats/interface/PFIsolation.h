#ifndef SoftDVDataFormats_PFIsolation_h
#define SoftDVDataFormats_PFIsolation_h

#include "DataFormats/PatCandidates/interface/PFIsolation.h"

// Implementation is the same as pat::PFIsolation.h
namespace SoftDV {
    class PFIsolation{
    public:
        PFIsolation() :
            chiso_(9999.), nhiso_(9999.), 
            phiso_(9999.), puiso_(9999.) {}

        PFIsolation(pat::PFIsolation patPFIso) :
            chiso_(patPFIso.chargedHadronIso()),
            nhiso_(patPFIso.neutralHadronIso()),
            phiso_(patPFIso.photonIso()),
            puiso_(patPFIso.puChargedHadronIso()) {}

        ~PFIsolation() {}

        float chargedHadronIso()   const { return chiso_; }
        float neutralHadronIso()   const { return nhiso_; }
        float photonIso()          const { return phiso_; }
        float puChargedHadronIso() const { return puiso_; }

    private:

        float chiso_; // charged hadrons from PV
        float nhiso_; // neutral hadrons
        float phiso_; // photons
        float puiso_; // pileup contribution (charged hadrons not from PV)

    };

}
#endif