import CombineHarvester.CombineTools.ch as ch

cb = ch.CombineHarvester()

inname = 'inputs.root'
backgrounds = ['WH_hzz','ZH_hzz','ggH_hzz','qqH_hzz','ttH_hzz','WH_hww','ZH_hww','ggH_hww','qqH_hww','ggZZ','qqZZ','VVV','TTV','ZX']
signals = ['sig']
mc = [x for x in backgrounds+signals if x!='ZX']
mc_hzz = [x for x in mc if 'hzz' in x]
mc_hww = [x for x in mc if 'hww' in x]
channels = ['4e','2e2m','4m']
cats = {
    '4e'  : [(0,'bin4e')],
    '2e2m': [(0,'bin2e2m')],
    '4m'  : [(0,'bin4m')],
}

for chan in channels:
    cb.AddObservations(['*'],   ['monoh'], ['13TeV'], [chan],              cats[chan])
    cb.AddProcesses(   ['*'],   ['monoh'], ['13TeV'], [chan], backgrounds, cats[chan], signal=False)
    cb.AddProcesses(   ['500'], ['monoh'], ['13TeV'], [chan], signals,     cats[chan], signal=True)

# systematics
# see: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/HiggsCombinationConventions

# TODO:
#   JES, mass_resol, ZX_mcscale, b_tag, EWcorr_VV

# lumi
# 2015: 2.3, 2016: 2.5, 2017: 2.3, 2018: 2.5
# naming: lumi_$ERA(_$YEAR) (for 2017,2018)
cb.cp().process(mc).AddSyst(cb, "lumi_$ERA_2017", "lnN", ch.SystMap()(1.023))

# scale uncertainties
# QCDscale_$X (X = ggH, qqH, VH, ttH, V, VV, ggVV, ttbar)
# for ggH see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SignalModelingTools
# or just the standard way of varying uR and uF up down by 2 (excluding both up or down by 2)
# TODO: recalculate
cb.cp().process(mc).AddSyst(
  cb, "QCDscale_ggH", "lnN", ch.SystMap('process')
  (['ggH_hzz','ggH_hww'], (1.039, 0.961))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_qqH", "lnN", ch.SystMap('process')
  (['qqH_hzz','qqH_hww'], (1.004, 0.997))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_VH", "lnN", ch.SystMap('process')
  (['ZH_hzz','ZH_hww'], (1.038, 0.970))
  (['WH_hzz','WH_hww'], (1.005, 0.993))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_ttH", "lnN", ch.SystMap('process')
  (['ttH_hzz','ttH_hww'], (1.058, 0.908))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_VV", "lnN", ch.SystMap('process')
  (['qqZZ'], (1.032, 0.958))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_ggVV", "lnN", ch.SystMap('process')
  (['ggZZ'], (1.1, 1.1))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_ttbar", "lnN", ch.SystMap('process')
  (['TTV'], (0.846, 1.146))
)

cb.cp().process(mc).AddSyst(
  cb, "QCDscale_monoH", "lnN", ch.SystMap('process')
  (['sig'], (1.035, 0.965))
)

# pdf
# pdf_gg, pdf_qqbar, and pdf_qg
# pdf_Higgs_$X (X = qqbar, gg, qg, ttH) for Higgs
# TODO: verify
cb.cp().process(mc).AddSyst(
  cb, "pdf_Higgs_qqbar", "lnN", ch.SystMap('process')
  (['WH_hzz','WH_hww'],   (1.019, 0.981))
  (['ZH_hzz','ZH_hww'],   (1.016, 0.984))
  (['qqH_hzz','qqH_hww'], (1.021, 0.979))
)

cb.cp().process(mc).AddSyst(
  cb, "pdf_Higgs_gg", "lnN", ch.SystMap('process')
  (['ggH_hzz','ggH_hww'],   (1.032, 0.968))
)

cb.cp().process(mc).AddSyst(
  cb, "pdf_Higgs_ttH", "lnN", ch.SystMap('process')
  (['ttH_hzz','ttH_hww'],   (1.036, 0.964))
)

cb.cp().process(mc).AddSyst(
  cb, "pdf_qqbar", "lnN", ch.SystMap('process')
  (['qqZZ'],   (0.966, 1.031))
  #(['VVV'],    ())
  (['TTV'],    (0.974, 1.025))
)

cb.cp().process(mc).AddSyst(
  cb, "pdf_gg", "lnN", ch.SystMap('process')
  #(['ggZZ'],   ())
  (['sig'],   (1.015, 0.985))
)


# underlying event
# UEPS

# branching ratios
cb.cp().process(mc_hzz).AddSyst(
  cb, "BR_hzz4l", "lnN", ch.SystMap()(1.02)
)



# efficiencies
# CMS_eff_$X_$YEAR (X = e, m, t, g, j, b)
# TODO: verify muon 1% + 0.5% per leg (id + iso)
cb.cp().process(mc).AddSyst(
  cb, "CMS_eff_m_2017", "lnN", ch.SystMap('channel')
    (['4m'],   1. + (4*(0.01**2+0.005**2))**0.5)
    (['2e2m'], 1. + (2*(0.01**2+0.005**2))**0.5)
)

# TODO: verify electron 4.5% per leg
cb.cp().process(mc).AddSyst(
  cb, "CMS_eff_e_2017", "lnN", ch.SystMap('channel')
    (['4e'],   1. + (4*(0.045**2))**0.5)
    (['2e2m'], 1. + (2*(0.045**2))**0.5)
)

# TODO: verify
cb.cp().process(mc).AddSyst(
  cb, "CMS_eff_trig_2017", "lnN", ch.SystMap()(1.02)
)


# fake
# FakeRate (for e/m jet fragmentation)
# CMS_fake_$X (X = e, m, t, g, j, b) for other

# energy scale
# CMS_scale_$X (X = e, m, t, g, j, met, b)
# see special not on jet energy
# these should be correlated with MET but aren't right now
# met energy scale
met_systs = ['JetEn','MuonEn','ElectronEn','UnclusteredEn','PhotonEn','JetRes']
for syst in met_systs: cb.cp().process(mc).AddSyst(cb, syst, "shape", ch.SystMap()(1.00))

# TODO: verify
cb.cp().process(mc).AddSyst(
  cb, "CMS_scale_m", "lnN", ch.SystMap('channel')
    (['4m'],   1. + (4*(0.0002**2))**0.5)
    (['2e2m'], 1. + (2*(0.0002**2))**0.5)
)

# TODO: verify
cb.cp().process(mc).AddSyst(
  cb, "CMS_scale_e", "lnN", ch.SystMap('channel')
    (['4e'],   1. + (4*(0.0015**2))**0.5)
    (['2e2m'], 1. + (2*(0.0015**2))**0.5)
)

# energy resolution
# CMS_res_$X (X = e, m, t, g, j, met, b)

# b tag
# CMS_btag_comb or (CMS_btag_light and CMS_btag_heavy)
# (or more complicated with iterative fit)

# load histograms
cb.cp().backgrounds().ExtractShapes(inname, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
cb.cp().signals().ExtractShapes(inname, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

# old way of doing bin by bin stats
#bbb = ch.BinByBinFactory()
#bbb.SetAddThreshold(0.0).SetMergeThreshold(1.0).SetFixNorm(False)
##bbb.MergeBinErrors(cb.cp().backgrounds())
#bbb.AddBinByBin(cb.cp().backgrounds(), cb)
#bbb.AddBinByBin(cb.cp().signals(), cb)

# TODO: autoMCStats through harvester...

ch.SetStandardBinNames(cb)

# save datacard
writer = ch.CardWriter('datacards/$TAG/$MASS/$ANALYSIS_$ERA.txt',
                       'datacards/$TAG/common/$ANALYSIS.input.root')
writer.WriteCards('combined', cb)
for chan in channels: writer.WriteCards(chan,cb.cp().channel([chan]))
