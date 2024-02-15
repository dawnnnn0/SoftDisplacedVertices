# CustomMiniAOD
MiniAOD customisation for soft displaced vertex search.

The production starts with the generation of MiniAOD starting with some AOD files. 
Datasets belonging to different eras and different Runs might have different conditions, calibrations, and detector alignment info associated with them. Therefore there are more than one configuration files.


`configuration` subdirectory contains the recommended config files we use for the production. `test`, `test_cfg`, `testK` contain some codes and other files when we test out some new features during the development phase. These are more like a user area within the repository.  

**Attention**: So far only 2018 configs are tested. Check them once again when MC and data of other years are included in the analysis.

`plugins` contain the C++ codes some of whose parameters are configurable to some extent. `python` directory contains the configurations for module initialisations (cfi), or configuration file fragments (cff). 


Below you can see an example to run a MiniAOD customisation.

```bash
cmsRun -n 4 CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py inputFiles="file:/path_to_local_file.root" outputFile="path_to output file.root" maxEvents=-1
```

MiniAOD outputs can be inspected through root. Just remember that the saved objects are C++ objects, so you need to know which variables and functions are available. e.g.

```c++
root [1] Events->Scan("recoTracks_FilterIsolateTracks_seed_MINI.obj->pt():SoftDVPFIsolations_FilterIsolateTracks_isolationDR03_MINI.obj->chargedHadronIso()")
***********************************************
*    Row   * Instance * recoTrack * SoftDVPFI *
***********************************************
*        0 *        0 * 0.5710884 *         0 *
*        0 *        1 * 0.7666415 *         0 *
*        0 *        2 * 2.0206983 *         0 *
*        0 *        3 * 2.4911582 * 2.5036621 *
*        0 *        4 * 0.5610689 *         0 *
*        0 *        5 * 0.9531079 *         0 *
Type <CR> to continue or q to quit ==> 

```