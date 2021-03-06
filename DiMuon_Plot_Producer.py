#!/usr/bin/env python
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime, sleep
from optparse import OptionParser
import array, ast
import math as m
from Btag_8TeV_Plots import *
import shutil
from run_details import this_run


trigger_effs =  { "150_Low":0.970,"150_High":0.972,
                  "200_Low":0.970,"200_High":0.972,
                  "275_Low":0.972,"275_High":0.973,
                  "325_Low":0.973,"325_High":0.973,
                  "375_Low":0.974,"375_High":0.972,
                  "475_Low":0.976,"475_High":0.973,
                  "575_Low":0.977,"575_High":0.974,
                  "675_Low":0.979,"675_High":0.977,
                  "775_Low":0.977,"775_High":0.973,
                  "875_Low":0.978,"875_High":0.978,
                  "975_Low":0.980,"975_High":0.978,
                  "1075_Low":0.977,"1075_High":0.979,}


# For 30/30 dimu selection
trigger_effs =  { "150_Low":0.989,"150_High":0.988,
                  "200_Low":0.989,"200_High":0.988,
                  "275_Low":0.989,"275_High":0.988,
                  "325_Low":0.989,"325_High":0.989,
                  "375_Low":0.989,"375_High":0.989,
                  "475_Low":0.989,"475_High":0.989,
                  "575_Low":0.989,"575_High":0.989,
                  "675_Low":0.990,"675_High":0.989,
                  "775_Low":0.989,"775_High":0.989,
                  "875_Low":0.990,"875_High":0.989,
                  "975_Low":0.990,"975_High":0.991,
                  "1075_Low":0.990,"1075_High":0.990}

settings = {
  "dirs":["150_200","200_275","275_325","325_375","375_475","475_575","575_675","675_775","775_875","875_975","975_1075","1075"],
  "Plots":["MHTovMET_all","HT_all","DiMuon_Mass_all", "MHT_all","AlphaT_all","JetMultiplicity_all","Number_Btags_all","CommonJetPt_all","CommonJetEta_all","MuPt_all","MuEta_all","SecondMuPt_all","SecondMuEta_all","MuPFIso_all","Number_Good_verticies_all"],
  "Lumo" : this_run()["mu_lumi"]*10.,
  "Webpage":"btag",
  "Category":"DiMuon",
  "WebBinning":["150_200","200_275","275_325","325_375","200_upwards","375_upwards"],
  "Misc":[],
  "MHTMET":"True",
  "Trigger":trigger_effs
  }

print ">> Opening directory:", this_run()["path_name"]
sleep(3)

rootpath = "../" + this_run()["path_name"]
njet_ext = ""
"""
rootpath = "NewConfig_RootFiles"
njet_ext = "_NJet"
"""
# dimuon_2d = {
#      "nMuon":("./"+rootpath+"/Muon_EWK"+njet_ext+".root","DiMuon_","Data","Muon","Inclusive"), 
#      "mc2":("./"+rootpath+"/Muon_EWK"+njet_ext+".root","DiMuon_","SMS","Muon","Inclusive"),
#     }
# dimuon_2d_data = {
#      "nMuon":("./"+rootpath+"/Muon_Data.root","DiMuon_","Data","Muon","Inclusive"), 
#     }

muon_plots = {
     "nMuon":("./"+rootpath+"/Muon_Data.root","DiMuon_","Data","Muon","Inclusive"), 
     "mc2":("./"+rootpath+"/Muon_WJets"+njet_ext+".root","DiMuon_","WJets","Muon","Inclusive"),
     "mc3":("./"+rootpath+"/Muon_TTbar.root","DiMuon_","TTbar","Muon","Inclusive"),
     "mc4":("./"+rootpath+"/Muon_Zinv.root","DiMuon_","Zinv","Muon","Inclusive"),
     "mc5":("./"+rootpath+"/Muon_DY"+njet_ext+".root","DiMuon_","DY","Muon","Inclusive"),
     "mc7":("./"+rootpath+"/Muon_DiBoson.root","DiMuon_","Di-Boson","Muon","Inclusive"),
     # "mc8":("./"+rootpath+"/Muon_QCD.root","DiMuon_","QCD","Muon","Inclusive"), 
     "mc9":("./"+rootpath+"/Muon_SingleTop.root","DiMuon_","Single_Top","Muon","Inclusive"),
    }

muon_one_btag_plots = {
     "nbMuon":("./"+rootpath+"/Muon_Data.root","btag_one_DiMuon_","Data","Muon","One"), 
     "mcb2":("./"+rootpath+"/Muon_WJets"+njet_ext+".root","btag_one_DiMuon_","WJets","Muon","One"),
     "mcb3":("./"+rootpath+"/Muon_TTbar.root","btag_one_DiMuon_","TTbar","Muon","One"),
     "mcb4":("./"+rootpath+"/Muon_Zinv.root","btag_one_DiMuon_","Zinv","Muon","One"),
     "mcb5":("./"+rootpath+"/Muon_DY"+njet_ext+".root","btag_one_DiMuon_","DY","Muon","One"),
     "mcb6":("./"+rootpath+"/Muon_SingleTop.root","btag_one_DiMuon_","Single_Top","Muon","One"),
     "mcb7":("./"+rootpath+"/Muon_DiBoson.root","btag_one_DiMuon_","Di-Boson","Muon","One"),
    }

muon_two_btag_plots = {

     "nbMuon":("./"+rootpath+"/Muon_Data.root","btag_two_DiMuon_","Data","Muon","Two"), 
     "mcb2":("./"+rootpath+"/Muon_WJets"+njet_ext+".root","btag_two_DiMuon_","WJets","Muon","Two"),
     "mcb3":("./"+rootpath+"/Muon_TTbar.root","btag_two_DiMuon_","TTbar","Muon","Two"),
     "mcb4":("./"+rootpath+"/Muon_Zinv.root","btag_two_DiMuon_","Zinv","Muon","Two"),
     "mcb5":("./"+rootpath+"/Muon_DY"+njet_ext+".root","btag_two_DiMuon_","DY","Muon","Two"),
     "mcb6":("./"+rootpath+"/Muon_SingleTop.root","btag_two_DiMuon_","Single_Top","Muon","Two"),
     "mcb7":("./"+rootpath+"/Muon_DiBoson.root","btag_two_DiMuon_","Di-Boson","Muon","Two"), 
    }

muon_zero_btag_plots = {
     "nbMuon":("./"+rootpath+"/Muon_Data.root","btag_zero_DiMuon_","Data","Muon","Zero"), 
     "mcb2":("./"+rootpath+"/Muon_WJets"+njet_ext+".root","btag_zero_DiMuon_","WJets","Muon","Zero"),
     "mcb3":("./"+rootpath+"/Muon_TTbar.root","btag_zero_DiMuon_","TTbar","Muon","Zero"),
     "mcb4":("./"+rootpath+"/Muon_Zinv.root","btag_zero_DiMuon_","Zinv","Muon","Zero"),
     "mcb5":("./"+rootpath+"/Muon_DY"+njet_ext+".root","btag_zero_DiMuon_","DY","Muon","Zero"),
     "mcb6":("./"+rootpath+"/Muon_SingleTop.root","btag_zero_DiMuon_","Single_Top","Muon","Zero"),
     "mcb7":("./"+rootpath+"/Muon_DiBoson.root","btag_zero_DiMuon_","Di-Boson","Muon","Zero"),  
    }

muon_morethanzero_btag_plots = {
     "nbMuon":("./"+rootpath+"/Muon_Data.root","btag_morethanzero_DiMuon_","Data","Muon","Zero"), 
     "mcb2":("./"+rootpath+"/Muon_WJets"+njet_ext+".root","btag_morethanzero_DiMuon_","WJets","Muon","Zero"),
     "mcb3":("./"+rootpath+"/Muon_TTbar.root","btag_morethanzero_DiMuon_","TTbar","Muon","Zero"),
     "mcb4":("./"+rootpath+"/Muon_Zinv.root","btag_morethanzero_DiMuon_","Zinv","Muon","Zero"),
     "mcb5":("./"+rootpath+"/Muon_DY"+njet_ext+".root","btag_morethanzero_DiMuon_","DY","Muon","Zero"),
     "mcb7":("./"+rootpath+"/Muon_DiBoson.root","btag_morethanzero_DiMuon_","Di-Boson","Muon","Zero"),
     "mcb9":("./"+rootpath+"/Muon_SingleTop.root","btag_morethanzero_DiMuon_","Single_Top","Muon","Zero"),
    }

if __name__=="__main__":
  a = Plotter(settings,muon_plots,jet_multiplicity = "True",make_ratio= "True")
  b = Plotter(settings,muon_morethanzero_btag_plots,jet_multiplicity = "True",make_ratio= "True")
  c = Plotter(settings,muon_two_btag_plots,jet_multiplicity = "True",make_ratio= "True")
  d = Plotter(settings,muon_zero_btag_plots,jet_multiplicity = "True",make_ratio= "True")
  e = Plotter(settings,muon_one_btag_plots,jet_multiplicity = "True",make_ratio= "True")
  """
  settings["Misc"] = ["NoLegend"]
  settings["Lumo"] = 1.0
  settings["Plots"] = ["MHT_vs_MET_all","MET_vs_MHTovMET_all"]
  #Plotter(settings,dimuon_2d,jet_multiplicity = "True",draw_data="False")
  settings["Plots"] = ["MET_vs_MHTovMET_all","MHT_vs_MET_all","MHTovMET_all","MHTovMET_Scaled_all","MET_all","MET_Corrected_all","MHT_all","MHT_FixedThreshold_all","JetMultiplicity_all","HT_all", "JetPt_all","JetEta_all"]
  """
  finish = Webpage_Maker(settings["Plots"],settings["WebBinning"],settings["Category"],option=settings["Webpage"])
  try :shutil.rmtree('./Plots')
  except OSError as exc: pass
