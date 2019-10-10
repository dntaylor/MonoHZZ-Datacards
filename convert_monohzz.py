from __future__ import print_function, division
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)

# define the samples
sampleMap = {
    'ZX': [
        'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8',
        'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
    ],
    'TTV': [
        'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
        'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
    ],
    'qqZZ': [
        'ZZTo2L2Nu_13TeV_powheg_pythia8',
        'ZZTo4L_13TeV_powheg_pythia8',
    ],
    'ggZZ': [
        'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8',
        'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
    ],
    'VVV': [
        'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8',
    ],
    'ggH_hww': [
        'GluGluHToWWTo2L2Nu_M125_13TeV_powheg2_JHUGenV714_pythia8',
    ],
    'qqH_hww': [
        'VBFHToWWTo2L2Nu_M125_13TeV_powheg2_JHUGenV714_pythia8',
    ],
    'WH_hww': [
        'HWplusJ_HToWWTo2L2Nu_WTo2L_M125_13TeV_powheg_pythia8_TuneCP5',
        'HWminusJ_HToWWTo2L2Nu_WTo2L_M125_13TeV_powheg_pythia8_TuneCP5',
    ],
    'ZH_hww': [
        'HZJ_HToWWTo2L2Nu_ZTo2L_M125_13TeV_powheg_jhugen714_pythia8_TuneCP5',
        'GluGluZH_HToWWTo2L2Nu_M125_13TeV_powheg_pythia8_TuneCP5',
    ],
    'ggH_hzz': [
        'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV7011_pythia8',
    ],
    'qqH_hzz': [
        'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUGenV7011_pythia8',
    ],
    'WH_hzz': [
        'WminusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8',
        'WplusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8',
    ],
    'ZH_hzz': [
        'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8',
    ],
    'ttH_hzz': [
        'ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUGenV7011_pythia8',
    ],
    'sig': [
        '2HDMplusa_MH3_500_MH4_150_MH2_500_MHC_500',
    ],
    'data_obs': [
        'SingleElectron',
        'SingleMuon',
        'DoubleEG',
        'DoubleMuon',
        'MuonEG',
    ],
}

# load the tfiles
channels = ['2e2m','4e','4m']
systs = [
    'JetEnUp','JetEnDn',
    'ElectronEnUp','ElectronEnDn',
    'MuonEnUp','MuonEnDn',
    'UnclusteredEnUp','UnclusteredEnDn',
    'PhotonEnUp','PhotonEnDn',
    'JetResUp','JetResDn',
    'FakeUp','FakeDn',
]
tfiles = {}
for c in channels:
    tfiles[c] = {}
    for s in sampleMap:
        for sample in sampleMap[s]:
            tfiles[c][sample] = ROOT.TFile.Open('monohzz/{}/output_{}.root'.format(c,sample))

def sumHists(name,*hists):
    hlist = ROOT.TList()
    for h in hists:
        if h: hlist.Add(h.Clone())
    if hlist.IsEmpty():
        print('No histograms for',name)
        return None
    hist = hists[0].Clone(name)
    hist.Reset()
    hist.Merge(hlist)
    return hist

hPath = 'hPFMET_10'
hSystPath = 'hPFMET_{syst}_10'
binning = array('d',[0,25,50,200,500,1000])

outname = 'inputs.root'
out = ROOT.TFile.Open(outname,'RECREATE')

hists = {}
for c in channels:
    hists[c] = {}
    for syst in ['']+systs:
        hists[c][syst] = {s:[] for s in sampleMap}
        for s in sampleMap:
            for sample in sampleMap[s]:
                name = 'h_{}_{}_{}_{}'.format(syst,c,s,sample)
                hist  = tfiles[c][sample].Get(hSystPath.format(syst=syst) if syst else hPath)
                if hist:
                    hists[c][syst][s] += [hist.Clone(name)]
        # sum the histograms
        for s in hists[c][syst]:
            hname = '{}_{}_{}'.format(syst,c,s)
            hist = sumHists(hname,*hists[c][syst][s])
            # bin the histogram
            if hist:
                hist = hist.Rebin(len(binning)-1,hname+'_rebin',binning)
            hists[c][syst][s] = hist
    d = out.mkdir('bin'+c)
    d.cd()
    for syst in ['']+systs:
        for s in hists[c][syst]:
            hist = hists[c][syst][s]
            if not hist: continue
            name = s+'_'+syst if syst else s
            if name.endswith('Dn'): name = name.replace('Dn','Down')
            hist.SetName(name)
            hist.SetTitle(name)
            hist.Write(name)
