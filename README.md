# MonoHZZ-Datacards
Datacard making utilities for MonoHZZ analysis.

Setup
-----
Follow instructions for Higgs Combine and Higgs Combine Harvester setup
https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
https://cms-analysis.github.io/CombineHarvester/
```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
pushd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.0.1
popd
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b clean
scram b -j 8
```

Then clone this repository
```bash
git clone https://github.com/dntaylor/MonoHZZ-Datacards.git
```

You can convert the output of the analysis step using
```bash
python MonoHZZ-Datacards/convert_monohzz.py
```
provided the ROOT files are available in a directory of the structure
`monohzz/[channel]` with `channel = 4e, 2e2m, 4m`.
This will produce an intermediate file `inputs.root`.

Next you can make the datacards with
```bash
python MonoHZZ-Datacards/make_monohzz.py
```
which will produce a `datacards` directory with the datacards.
