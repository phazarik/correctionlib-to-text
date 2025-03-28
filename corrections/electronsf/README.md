## Electron POG corrections
|Correction type|File| Source file|Correction name|
|--|--|--|--|
|ID|`electron_id_sf.txt`|[`electron.json`](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2018_UL_electron.html)|`UL-Electron-ID-SF`|
---
#### File structure :
```
Campaign >> eta_low >> eta_high >> pT_low >> pT_high >> phi_low >> phi_high >> SFdown >> SF >> SFup
```
#### Input information:
- Available campaigns: `2018_UL`, `2017_UL`, `2016postVFP_UL`, `2016preVFP_UL`
- pT bins: `[10.0, 20.0, 35.0, 50.0, 100.0, inf]`
- eta bins: `[-inf, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, inf]`
- phi bins: `[-inf, -1.2, -0.8, inf]` (Used in Run3Summer23 only.)