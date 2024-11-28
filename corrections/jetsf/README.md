## Jet POG corrections

|Correction type|File| Source file|Correction name (2018)|
|--|--|--|--|
|Jet Energy Correction|`jet_jec_sf.txt`|[`jet_jerc.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jet_jerc.html)|`Summer19UL18_V5_MC_Total_AK4PFchs`|
|Jet Energy Resolution|`jet_jer_sf.txt`|[`jet_jerc.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jet_jerc.html)|`Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs`|
|Jet pT Resolution |`jet_ptres_sf.txt`|[`jet_jerc.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jet_jerc.html)|`Summer19UL18_JRV2_MC_PtResolution_AK4PFchs`|

---
### Jet energy correction
Correct each Jet 4-vector using the information from `jet_jec_sf.txt` based on the pT and eta of the jet for each campaign. The text file is organised as follows:
```
Campaign >> eta_low >> eta_high >> pT_low >> pT_high >> SFdown >> SF >> SFup
```
In nanoAOD, the Jets are corrected by default, and hence the nominal SF is 1. However, the up and down systematic variations are needed for calculation of systematic uncertainty. These are given in the following pT and eta bins.
- pT bins : 
- eta bins: `[-5.4, -5.0, -4.4, -4.0, -3.5, -3.0, -2.8, -2.6, -2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.4, 5.0, 5.4]`

---
### Jet energy resolution correction
It requires two types of corrections to each Jet 4-vector. The first type is a scale factor in eta bins from `jet_jer_sf.txt`. This text file is organised as follows:.
```
Campaign >> eta_low >> eta_high >> JERdown >> JER >> JERup
```
The following the the eta bins.

- eta bins = `[-5.191, -3.139, -2.964, -2.853, -2.65, -2.5, -2.322, -2.043, -1.93, -1.74, -1.305, -1.131, -0.783, -0.522, -0.0, 0.522, 0.783, 1.131, 1.305, 1.74, 1.93, 2.043, 2.322, 2.5, 2.65, 2.853, 2.964, 3.139, 5.191]`

The second type is a calculation of sigma JER from `jet_ptres_sf.txt`, which is done by taking values of eta and rho, and evaluating a function for each pT. Since I am writing a text file, I picked bins of pT as given below. In principle, we can have as fine binning as we want, but I am choosing the same binning as JER.
- pT bins chosen manually - `[9.0, 11.0, 13.5, 16.5, 19.5, 22.5, 26.0, 30.0, 34.5, 40.0, 46.0, 52.5, 60.0, 69.0, 79.0, 90.5, 105.5, 123.5, 143.0, 163.5, 185.0, 208.0, 232.5, 258.5, 286.0, 331.0, 396.0, 468.5, 549.5, 639.0, 738.0, 847.5, 968.5, 1102.0, 1249.5, 1412.0, 1590.5, 1787.0, 2003.0, 2241.0, 2503.0, 2790.5, 3107.0, 3455.0, 3837.0, 4257.0, 4719.0, 5226.5, 5784.0, 6538.0]`

This file is organised as follows:.
```
Campaign >> eta_low >> eta_high >> pT_low >> pT_high >> rho_low >> rho_high >> sigmaJER
```
In this case, the uncertainties are not given in the json file (since the evaluation is in functional form). However, the parameters of the function changed in eta and rho bins mentioned below:

- eta bins = `[-4.7, -3.2, -3.0, -2.8, -2.5, -2.3, -2.1, -1.9, -1.7, -1.3, -1.1, -0.8, -0.5, 0.0, 0.5, 0.8, 1.1, 1.3, 1.7, 1.9, 2.1, 2.3, 2.5, 2.8, 3.0, 3.2, 4.7]`
- rho bins = `[0.0, 7.22, 13.26, 19.3, 25.33, 31.37, 37.4, 90.0]`

Both of these corrections, along with Jet flavor are used to calculate the overall JER correction.   