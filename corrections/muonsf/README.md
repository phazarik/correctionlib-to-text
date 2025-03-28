## Muon POG corrections

|Correction type|File| Source file|Correction name|
|--|--|--|--|
|ID SF|`muon_id_sf.txt` |[`muon_Z_v2.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2018_UL_muon_Z.html) (MUO POG)| `NUM_MediumID_DEN_genTracks`
|Isolation SF|`muon_iso_sf.txt`|[`muon_Z_v2.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2018_UL_muon_Z.html) (MUO POG)| `NUM_TightRelIso_DEN_MediumID`

---
#### File structure [both]:
```
Campaign >> eta_low >> eta_high >> pT_low >> pT_high >> SFdown >> SF >> SFup
```
#### Input information:
- Available campaigns: `2018_UL`, `2017_UL`, `2016postVFP_UL`, `2016preVFP_UL`
- pT bins: `[15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, inf]`
- abs(eta) bins: `[0.0, 0.9, 1.2, 2.1, 2.4]` 