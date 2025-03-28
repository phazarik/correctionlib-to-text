## b-Jet POG efficiencies


|Efficiency type|File| Source file|Correction name (2018)|
|--|--|--|--|
|Jet Energy Correction|`bjet_comb_and_incl_eff.txt`|[`btagging.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2018_UL_btagging.html)|`deepJet_comb`, `deepJet_incl`|
|Jet Energy Resolution|`bjet_mujets_and_incl_eff.txt`|[`btagging.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2018_UL_btagging.html)|`deepJet_mujets`, `deepJet_incl`|


Both of these efficiencies are essentially the same; just the methods are different (for b and c jets). The text files are organised as follows.
```
Campaign >> eta_low >> eta_high >> pT_low >> pT_high >> flavor >> effdown >> eff >> effup
```
This is a function-based evaluation, and the pT-eta bins are directly taken from the json file.
- pT bins: `[20.0, 30.0, 50.0, 70.0, 100.0, 140.0, 200.0, 300.0, 600.0, 1000.0]`
- abs(eta) bins: `[0, 2.5]`