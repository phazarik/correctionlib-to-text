# Correctionlib to text

Correctionlib is a library that provides a standardized interface for evaluating physics object correction factors and scale factors defined in JSON format [[see documentation](https://cms-nanoaod.github.io/correctionlib/)]. It supports python and C++ (that I know of). It returns correction parameters typically in bins of pT and eta of the physics objects. I designed this correctionlib-to-text converter for systems not compatible with correctionlib, where I flatten the information organised in json format and write down into text files with a pandas dataframe structure. These text files can be parsed easily into C++ or python based analysis framework. Instructions for each types of corrections are given in the respective directories:

- [`corrections/electronsf`](https://github.com/phazarik/correctionlib-to-text/tree/main/corrections/electronsf)
- [`corrections/muonsf`](https://github.com/phazarik/correctionlib-to-text/tree/main/corrections/muonsf)
- [`corrections/jetsf`](https://github.com/phazarik/correctionlib-to-text/tree/main/corrections/jetsf)
-  [`/corrections/bjeteff`](https://github.com/phazarik/correctionlib-to-text/tree/main/corrections/bjeteff)


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