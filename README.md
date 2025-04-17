# Correctionlib to text

Correctionlib is a library that provides a standardized interface for evaluating physics object correction factors and scale factors defined in JSON format [[see documentation](https://cms-nanoaod.github.io/correctionlib/)]. It supports Python and C++ (that I know of). It returns correction parameters typically in bins of pT and eta of the physics objects. I designed this correctionlib-to-text converter for systems not compatible with correctionlib, where I flatten the information organized in JSON format and write it down into text files with a pandas dataframe structure. These text files can be parsed easily into C++ or Python-based analysis frameworks.

### Important links
- [Correction factors released by POGs](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration) in JSON format (needs CERN user account)
- [Summary of JSON files from POGs](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/) (how to feed inputs)

### Required dependencies
- correctionlib [can be installed with `conda install correctionlib`]
- json
- pandas
- numpy

### Choices that I made while creating the text files
- Medium ID corrections for muon.
- Medium working point for b-jets.

---
Feel free to use and modify this project as per your needs. Contact me if you need help.