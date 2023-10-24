// This producer produces the table of LLP information
// Also, it makes the mapping between LLP and all the gen level decay products

// system include files
#include <memory>
#include <queue>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

class LLPTableProducer : public edm::stream::EDProducer<> {
  public:
    explicit LLPTableProducer(const edm::ParameterSet&);
    ~LLPTableProducer() override;

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    void beginStream(edm::StreamID) override;
    void produce(edm::Event&, const edm::EventSetup&) override;
    void endStream() override;

    const edm::EDGetTokenT<std::vector<reco::GenParticle>> genToken_;
    const std::string LLPName_;
    const std::string LLPDoc_;
    const int LLPid_;
    const int LSPid_;
    const edm::EDGetTokenT<reco::VertexCollection> pvToken_;
    bool debug;
};

LLPTableProducer::LLPTableProducer(const edm::ParameterSet& params)
  : genToken_(consumes<std::vector<reco::GenParticle>>(params.getParameter<edm::InputTag>("src"))),
    LLPName_(params.getParameter<std::string>("LLPName")),
    LLPDoc_(params.getParameter<std::string>("LLPDoc")),
    LLPid_(params.getParameter<int>("LLPid_")),
    LSPid_(params.getParameter<int>("LSPid_")),
    pvToken_(consumes<reco::VertexCollection>(params.getParameter<edm::InputTag>("pvToken"))),
    debug(params.getParameter<bool>("debug"))
{
  produces<nanoaod::FlatTable>("LLPs");
  produces<nanoaod::FlatTable>("GenPart");
}

LLPTableProducer::~LLPTableProducer() {}

void LLPTableProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  edm::Handle<reco::GenParticleCollection> genParticles;
  iEvent.getByToken(genToken_, genParticles);

  edm::Handle<reco::VertexCollection> primary_vertices;
  iEvent.getByToken(pvToken_, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  std::vector<int> llp_idx = SoftDV::FindLLP(genParticles, LLPid_, LSPid_, debug);
  std::vector<float> llp_pt, llp_eta, llp_phi, llp_mass, llp_ctau, llp_decay_x, llp_decay_y, llp_decay_z;
  std::vector<int> llp_pdgId, llp_status, llp_statusFlags;

  std::vector<int> genpart_llpidx(genParticles->size(), -1);

  if (debug)
    std::cout << "Start the LLP loop." << std::endl;
  //for (const auto& llp : llps){
  for (size_t illp=0; illp<llp_idx.size(); ++illp){
    if (debug)
      std::cout << "For LLP " << illp << std::endl;
    const reco::GenParticle& llp = genParticles->at(llp_idx[illp]);
    if (debug)
      std::cout << "LLP get." << std::endl; 
    llp_pt.push_back(llp.pt());
    llp_eta.push_back(llp.eta());
    llp_phi.push_back(llp.phi());
    llp_mass.push_back(llp.mass());
    llp_pdgId.push_back(llp.pdgId());
    llp_status.push_back(llp.status());
    llp_statusFlags.push_back( llp.statusFlags().isLastCopyBeforeFSR()             * 16384 +llp.statusFlags().isLastCopy()                           * 8192  +llp.statusFlags().isFirstCopy()                          * 4096  +llp.statusFlags().fromHardProcessBeforeFSR()             * 2048  +llp.statusFlags().isDirectHardProcessTauDecayProduct()   * 1024  +llp.statusFlags().isHardProcessTauDecayProduct()         * 512   +llp.statusFlags().fromHardProcess()                      * 256   +llp.statusFlags().isHardProcess()                        * 128   +llp.statusFlags().isDirectHadronDecayProduct()           * 64    +llp.statusFlags().isDirectPromptTauDecayProduct()        * 32    +llp.statusFlags().isDirectTauDecayProduct()              * 16    +llp.statusFlags().isPromptTauDecayProduct()              * 8     +llp.statusFlags().isTauDecayProduct()                    * 4     +llp.statusFlags().isDecayedLeptonHadron()                * 2     +llp.statusFlags().isPrompt()                             * 1);

    if (debug)
      std::cout << "basic variables" << std::endl;
    // Now determine the LLP decay point
    if (llp.numberOfDaughters()==0){
      throw cms::Exception("LLPTableProducer") << "LLP has no Daughters!";
    }
    std::cout << "LLP has " << llp.numberOfDaughters() << " daughters."  << std::endl;
    if (debug)
    {
      for (size_t idau=0; idau<llp.numberOfDaughters(); ++idau){
        std::cout << "LLP daughter " << idau << " ID " << llp.daughter(idau)->pdgId() << std::endl;
        std::cout << llp.daughter(idau)->vertex().x() << std::endl;
      }
    }
    auto decay_point = llp.daughter(0)->vertex();
    std::cout << "decay point" << std::endl;
    llp_decay_x.push_back(decay_point.x());
    llp_decay_y.push_back(decay_point.y());
    llp_decay_z.push_back(decay_point.z());
    std::cout << "decay / ctau" << std::endl;

    math::XYZVector flight = math::XYZVector(decay_point) - math::XYZVector(primary_vertex->position());
    auto polarp4 = llp.polarP4();
    float ctau = std::sqrt(flight.Mag2())/polarp4.Beta()/polarp4.Gamma();
    llp_ctau.push_back(ctau);
    if (debug)
      std::cout << "decay variables" << std::endl;

    // Get the LLP decay products
    // FIXME: Why does this results in Seg. Fault?
    std::vector<int> llp_daus = SoftDV::GetDaughters(llp_idx[illp], genParticles, debug);

    //if (debug)
    //  std::cout << "Start looking for daughters." << std::endl;
    //std::queue<reco::GenParticleRef> gen_daughter_queue;
    //std::vector<int> processed_gen_key;
    //std::vector<int> llp_daus;
    ////reco::GenParticleCollection llp_daus;
    //std::vector<reco::GenParticle> gtks;
    ////const auto& llp_ref = SoftDV::get_gen(&llp, genParticles);
    //const auto& llp_ref = reco::GenParticleRef(genParticles,llp_idx[illp]);
    //if (debug)
    //  std::cout << "Get LLP reference." << std::endl;
    //if (!llp_ref)
    //  std::cout << "CANNOT FIND LLP REFERENCE!" << std::endl;
    //gen_daughter_queue.push(llp_ref);
    //processed_gen_key.push_back(llp_ref.key());
    //while (!gen_daughter_queue.empty()) {
    //  reco::GenParticleRef dau = gen_daughter_queue.front();
    //  if (debug) {
    //    std::cout << "  Daughter " << dau->pdgId() << " status " << dau->status() << " charge " << dau->charge() << std::endl;
    //  }
    //  gen_daughter_queue.pop();
    //  if ( (dau->status()==1) && (dau->charge()!=0)){
    //    if (dau.isNonnull()){
    //      llp_daus.push_back(dau.key());
    //      //llp_daus.push_back(*(dau.get()));
    //    }
    //    if (debug){
    //      std::cout << "  Final status gen daughter added. ID " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
    //    }
    //    if (dau->numberOfDaughters()>0){
    //      std::cout << "GenProducer: Gen daughter with status 1 has daughters!" << std::endl;
    //    }
    //    continue;
    //  }
    //  for (size_t idau=0; idau<dau->numberOfDaughters(); ++idau){
    //    const auto& gendau = SoftDV::get_gen(dau->daughter(idau), genParticles);
    //    if (!gendau)
    //      continue;
    //    int gendau_key = gendau.key();
    //    if (debug){
    //      std::cout << "    daughter " << gendau->pdgId() << " status " << gendau->status() << " key " << gendau_key << std::endl;
    //    }
    //    if(std::find(processed_gen_key.begin(), processed_gen_key.end(), gendau_key) != processed_gen_key.end()) {
    //      if (debug)
    //        std::cout << "     Is was processed before so skipping..." << std::endl;
    //      continue;
    //    }
    //    gen_daughter_queue.push(gendau);
    //    processed_gen_key.push_back(gendau.key());
    //  }
    //
    //}

    for (int igen:llp_daus){
      genpart_llpidx[igen] = illp;
    }

  }

  std::cout << "Finish LLP loop." << std::endl;

  // Flat table for LLPs
  auto llpTable = std::make_unique<nanoaod::FlatTable>(llp_idx.size(), LLPName_, false);
  llpTable->addColumn<float>("pt", llp_pt, "pt", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("eta", llp_eta, "eta", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("phi", llp_phi, "phi", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("mass", llp_mass, "mass", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("ctau", llp_ctau, "ctau", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("decay_x", llp_decay_x, "x position of LLP decay in cm", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("decay_y", llp_decay_y, "y position of LLP decay in cm", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<float>("decay_z", llp_decay_z, "z position of LLP decay in cm", nanoaod::FlatTable::FloatColumn, 10);
  llpTable->addColumn<int>("pdgId", llp_pdgId, "pdgID of LLP", nanoaod::FlatTable::IntColumn);
  llpTable->addColumn<int>("status", llp_status, "status of LLP", nanoaod::FlatTable::IntColumn);
  llpTable->addColumn<int>("statusFlags", llp_statusFlags, "gen status flags stored bitwise, bits are: 0 : isPrompt, 1 : isDecayedLeptonHadron, 2 : isTauDecayProduct, 3 : isPromptTauDecayProduct, 4 : isDirectTauDecayProduct, 5 : isDirectPromptTauDecayProduct, 6 : isDirectHadronDecayProduct, 7 : isHardProcess, 8 : fromHardProcess, 9 : isHardProcessTauDecayProduct, 10 : isDirectHardProcessTauDecayProduct, 11 : fromHardProcessBeforeFSR, 12 : isFirstCopy, 13 : isLastCopy, 14 : isLastCopyBeforeFSR, ", nanoaod::FlatTable::IntColumn);

  auto genPartTable = std::make_unique<nanoaod::FlatTable>(genParticles->size(), "SDVGenPart", false, true);
  genPartTable->addColumn<int>("LLPIdx",genpart_llpidx, "LLP index", nanoaod::FlatTable::IntColumn);

  iEvent.put(std::move(llpTable), "LLPs"); 
  iEvent.put(std::move(genPartTable), "GenPart");
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void LLPTableProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void LLPTableProducer::endStream() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void LLPTableProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(LLPTableProducer);
