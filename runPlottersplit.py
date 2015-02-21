#!/usr/bin/env python

##############################################################################################################
#                                                                                                            #
#                                        QIE10 Robot data Plotter                                            #
#                                                                                                            #
#                                           FNAL-LPC, Dic 2014                                               # 
#                                                                                                            #
# Usage: python runPlotter.py QIE10rootfile.root"                                                            #
#                                                                                                            #
# TH1F. In order to make your th1d plots you need to create 3 files and fill them with columns as following: #
#                                                                                                            #
#           qie10_histograms.txt: "Histogramname"                                                            # 
#           qie10_labels.txt: "LabelinXaxis LabelinYaxis"                                                    #
#           qie10_bins.txt: "NumberofBins"                                                                   #
#                                                                                                            #
#                                                                                                            #
#                                                                                                            #
##############################################################################################################

import ROOT
from ROOT import *
import os,sys, pprint, numpy


def stats1d():
    # Plot statistics using a different style
    gStyle.SetOptTitle(0)
    gStyle.SetStatX(0.89)
    gStyle.SetStatY(0.89)
    gStyle.SetOptStat(0) 
    gStyle.SetStatBorderSize(0);

def caption():

	#Volt_Rref< 0.39 caption
    caption1=ROOT.TLatex()
    caption1.SetTextSize(0.069)
    caption1.SetTextFont(42)
    caption1.SetNDC()
    caption1.DrawLatex(0.75,0.95,'Chips, Volt_Rref<0.39')

    #Volt_Rref > 0.39 caption
    caption2=ROOT.TLatex()
    caption2.SetTextSize(0.069)
    caption2.SetTextFont(42)
    caption2.SetNDC()
    caption2.DrawLatex(0.75,0.89,'#color[2]{Chips, Volt_Rref>0.39}')

    # QIE caption
    caption3=ROOT.TLatex()
    caption3.SetTextSize(0.069)
    caption3.SetTextFont(42)
    caption3.SetNDC()
    caption3.DrawLatex(0.15,0.92,'QIE10 Chip Test')

def drawplot(filename=None,h=None,XLabel=None,YLabel=None,nbins=None):


    # Get the information from the ROOT file
    f = ROOT.TFile(filename, "open")
    t = TTree()
    t = f.Get("ChipData")
    htemp = TH1F()
   
    #Select the histogram you want to plot. If you histogram is ADCDNL, Sum4DNL or TDCVertOffset, it is plotted separately.
    if (h == 'ADCDNL') or  (h == 'Sum4DNL') or (h =='TDCVertOffset'):

      c = TCanvas("c","c")	

      #Quick draw in order to not to consider in the histograms some chips which are working very well using the cuts defined below
      t.Draw(h,"(Volt_Rref<0.39) && (IDCset0a < 1.21) && (ImpDiff_RinSel0 < 0.0048) &&  (SumDAC4 > 1200) && (Int_R0S0_CID3 < 60) && (Int_R1S1_CID0 < 225) && (Int_R2S1_CID0 < 2500)  && (Int_R3S1_CID0 < 18000) && (Int_R1S1_CID0 < 600) && (Slope_R1S0_CID0 < 30) && (Slope_R2S0_CID2 < 400) && (Slope_R2S1_CID0 < 425)" )	
      htemp = gPad.GetPrimitive("htemp")
      htemp.Rebin(5)
      htemp.GetXaxis().SetTitle(XLabel)
      htemp.GetYaxis().SetTitle(YLabel)
      htemp.GetYaxis().SetTitleSize(0.039)
      htemp.SetLineColor(kBlack)

      del htemp 

      ##Quick draw in order to not to consider in the histograms some chips which are working very well using the cuts defined below
      t.Draw(h,"(Volt_Rref>0.39) && (IDCset0a < 1.21) && (ImpDiff_RinSel0 < 0.0048) &&  (SumDAC4 > 1200) && (Int_R0S0_CID3 < 60) && (Int_R1S1_CID0 < 225) && (Int_R2S1_CID0 < 2500)  && (Int_R3S1_CID0 < 18000) && (Int_R1S1_CID0 < 600) && (Slope_R1S0_CID0 < 30) && (Slope_R2S0_CID2 < 400) && (Slope_R2S1_CID0 < 425)","sames" )	
      htemp = gPad.GetPrimitive("htemp")
      htemp.GetXaxis().SetTitle(XLabel)
      htemp.GetYaxis().SetTitle(YLabel)
      htemp.GetYaxis().SetTitleSize(0.039)
      htemp.SetLineColor(kRed)
      caption()


      c.SaveAs( h + '.pdf' )
      del c

    else:

      #Quick draw in order to not to consider in the histograms some chips which are working very well using the cuts defined below
      t.Draw(h,"(IDCset0a < 1.21) && (ImpDiff_RinSel0 < 0.0048) &&  (SumDAC4 > 1200) && (Int_R0S0_CID3 < 60) && (Int_R1S1_CID0 < 225) && (Int_R2S1_CID0 < 2500)  && (Int_R3S1_CID0 < 18000) && (Int_R1S1_CID0 < 600) && (Slope_R1S0_CID0 < 30) && (Slope_R2S0_CID2 < 400) && (Slope_R2S1_CID0 < 425)" )
      htemp = gPad.GetPrimitive("htemp")
      mn = htemp.GetXaxis().GetXmin()
      mx = htemp.GetXaxis().GetXmax()
      bins=int(nbins)

      #Create two histograms and fill them with the information you got above
      h1d = TH1F("h1d",h,bins,mn,mx)
      h2d = TH1F("h2d",h,bins,mn,mx)  
      nentry = t.GetEntries()  	
      for i in range(0,nentry):
         t.GetEntry(i)
         cut=getattr(t,"Volt_Rref") 
         var=getattr(t,"%s"%h) 
         if cut < 0.39:
           h1d.Fill(var)
         else:   
           h2d.Fill(var) 
      del htemp

      h1d.Sumw2()
      h2d.Sumw2()

      #Define error bars in h1d histograms
      for bin in range(0, h1d.GetNbinsX()):
         h1d.SetBinError(bin, 0.)
         error1 = sqrt(h1d.GetBinContent(bin))
         if error1 != 0: 
           h1d.SetBinError(bin, error1)
      #Define error bars in h2d histograms
      for bin in range(0, h2d.GetNbinsX()):
         h2d.SetBinError(bin, 0.)
         error2 = sqrt(h2d.GetBinContent(bin))
         if error2 != 0:
          h2d.SetBinError(bin, error2)

      #Create and define the comparison plot
      hdiv = TH1F()
      hdiv.Sumw2()
      hdiv = h1d.Clone()
      hdiv.Divide(h2d)

      #Draw everything using a canvas
      c=TCanvas('c','c')
      c.Divide(1,2,0,0)

      #First pad
      c.cd(1)
      c.GetPad(1).SetBottomMargin(0.001);
      ##Set Labels and Sizes in the plots
      h1d.SetLineColor(kBlack)
      h1d.SetLineWidth(1)
      h2d.SetLineColor(kRed)
      h2d.SetLineWidth(1)

      ##Set other stat style
      stats1d()

      ##Choose the order of the Draw option and Draw the histogram
      max1 = h1d.GetMaximum()
      max2 = h2d.GetMaximum()
      if max1 > max2:
      	h1d.GetXaxis().SetTitle(XLabel)
        h1d.GetYaxis().SetTitle(YLabel)
        h1d.GetYaxis().SetTitleSize(0.05)
        h1d.GetYaxis().SetLabelSize(0.05)
        h1d.DrawNormalized("hist e0")
        hdiv.GetXaxis().SetTitle(h1d.GetXaxis().GetTitle())  
        h2d.DrawNormalized("hist same e0")
      else:
      	h2d.GetXaxis().SetTitle(XLabel)
        h2d.GetYaxis().SetTitle(YLabel)
        h2d.GetYaxis().SetTitleSize(0.05)
        h2d.GetYaxis().SetLabelSize(0.05)
        h2d.DrawNormalized("hist e0")
        hdiv.GetXaxis().SetTitle(h2d.GetXaxis().GetTitle())  
        h1d.DrawNormalized("hist same e0")      
      
      ##Add a caption
      caption()

      #Second pad
      c.cd(2)
      c.GetPad(2).SetGridy()

      ##Draw your comparison plot
      hdiv.Draw("e")

      ##Add title and other features
      hdiv.SetLineWidth(1)
      hdiv.GetYaxis().SetTitle("#frac{Volt_Rref < 0.39}{Volt_Rref > 0.39}")  
      hdiv.GetXaxis().SetTitleSize(0.045)
      hdiv.GetXaxis().SetLabelSize(0.045)
      hdiv.GetYaxis().SetTitleSize(0.045)
      hdiv.GetYaxis().SetLabelSize(0.045)

      ##save and delete
      c.SaveAs( h + '.pdf' )
      del c

def main(argv=None):

    #Look for the root file 
    filename = sys.argv[1]
    print "... processing robotdata:", filename

    #Error message 
    from os import path
    if not path.isfile(filename):
        print "Help, file doesnt exist"
        exit(-1)

    #Open text files with information for the plots and make the respective array
    histograms = numpy.loadtxt('qie10_histos.txt', dtype='string')
    labels = numpy.loadtxt('qie10_labels.txt', dtype='string')
    bins = numpy.loadtxt('qie10_bins.txt', dtype=int)
    nh = len(histograms)

    #Make a loop over all the histograms
    for i in range(0,nh):

           #Get the parameteter h,Locut,Hicut,Xunit,Yunits from the arrays
           Xunits = labels[i,0]
           Yunits = labels[i,1]
           numbins = bins[i]
           histoname = histograms[i]
           drawplot(filename=filename,h=histoname,XLabel=Xunits,YLabel=Yunits,nbins=numbins)

    #Save plots
    os.system("mkdir qie10split")
    os.system("cp *.pdf ./qie10split")
    os.system("rm *.pdf")   

if __name__ == "__main__":
    sys.exit(main())

