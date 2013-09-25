import FWCore.ParameterSet.Config as cms

process = cms.Process("electrons")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("RecoEgamma.EgammaElectronProducers.gsfElectronSequence_cff")
process.load("Configuration.StandardSequences.DigiToRaw_cff")
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

###### HERE IS THE PART THAT YOU WANT TO CONFIGURE #######
usePFClusters = True
##########################################################

if usePFClusters:
    process.ecalDrivenElectronSeeds.barrelSuperClusters = 'particleFlowSuperClusterECAL'
    process.ecalDrivenElectronSeeds.endcapSuperClusters = 'particleFlowSuperClusterECAL'

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
     '/store/relval/CMSSW_7_0_0_pre3/RelValSingleElectronPt10/GEN-SIM-DIGI-RAW-HLTDEBUG/PRE_ST62_V8-v1/00000/E60C2BAF-8414-E311-AC44-003048678B7C.root'
    )
)

process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *', 
                                           'keep *_*_*_electrons', 
                                           'keep *HepMCProduct_*_*_*',
                                           'keep *_genParticles_*_*',
                                           'keep *_addPileupInfo_*_*'
                                           ),
    fileName = cms.untracked.string('electrons.root')
)



process.localreco = cms.Sequence(process.trackerlocalreco+
                                 process.muonlocalreco+
                                 process.calolocalreco+
                                 process.castorreco)

process.gloabalreco = cms.Sequence(process.offlineBeamSpot*
                                   process.recopixelvertexing*
                                   process.trackingGlobalReco*
                                   process.hcalGlobalRecoSequence*
                                   process.particleFlowCluster*
                                   process.ecalClusters*
                                   process.caloTowersRec*
                                   process.vertexreco*
                                   process.egammaGlobalReco)

process.reducedRecHits = cms.Sequence (process.reducedEcalRecHitsSequence *
                                       process.reducedHcalRecHitsSequence )

process.highlevelreco = cms.Sequence(process.egammaHighLevelRecoPrePF*
                                     process.particleFlowReco*
                                     process.egammaHighLevelRecoPostPF*
                                     process.reducedRecHits)

process.p = cms.Path(process.DigiToRaw*
                     process.RawToDigi*
                     process.localreco*
                     process.globalreco*
                     process.highlevelreco)

process.outpath = cms.EndPath(process.out)
process.GlobalTag.globaltag = 'PRE_ST62_V8::All'


