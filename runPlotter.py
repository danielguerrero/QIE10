#!/usr/bin/env python

##############################################################################################################
#                                                                                                            #
#                                        QIE10 Robot data Plotter                                            #
#                                                                                                            #
#                                           FNAL-LPC, Dic 2014                                               # 
#                                                                                                            #
# Usage: python runPlotter.py file.root"                                                                     #
#                                                                                                            #
# TH1F. In order to make your th1d plots you need to create 3 files and fill them with columns as following: #
#                                                                                                            #
#           qie10_histograms.txt: "Histogramname"                                                            # 
#           qie10_cuts.txt: "ValueLowCut ValueHiCut"                                                         #
#           qie10_labels.txt: "LabelinXaxis LabelinYaxis"                                                    #
#           qie10_bins.txt:"Nbins"                                                                           # 
#                                                                                                            #
# TH2F. In order to make your th2d plots you need to create an additional .txt file and it is not            #
#       necessary to have the cuts file:                                                                     #
#                                                                                                            #
#           qie10_2dhistograms.txt: "HistonameXaxis HistonameYaxis"                                          #
#                                                                                                            #
#                                                                                                            #
##############################################################################################################

import ROOT
from ROOT import *
import os,sys, pprint, numpy
from numpy import *


def runPlotter():

    #Look for the root file and ask the things you want to plot
    filename = sys.argv[1]
    print "... processing chips data from:", filename

    #Ask about the features in the plots
    th1f  = raw_input("Would you like to make TH1D plots (Yes/No)? ")
    if th1f == 'Yes':
             cutbars = raw_input("  Would you like to add the cut bars to the plots (Yes/No)? ")
    else:
             cutbars ='No'
    th2f  = raw_input("Would you like to make TH2D plots (Yes/No)? ")

    #Error message
    from os import path
    if not path.isfile(filename):
        print "Help, file doesnt exist"
        exit(-1)

    return th1f,cutbars,th2f,filename

def openfile(filename=None):

    f = ROOT.TFile(filename, "read")
    t = TTree()
    t = f.Get("ChipData")
    return f,t
    
def stats1d():
    # Plot statistics using a different style
    gStyle.SetOptTitle(0)
    gStyle.SetStatX(0.89)
    gStyle.SetStatY(0.89)
    gStyle.SetOptStat(111110)
    gStyle.SetStatBorderSize(0);

def stats2d():
    # Plot statistics using a different style
    gStyle.SetOptTitle(1)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.34)
    gStyle.SetStatY(0.85)
    gStyle.SetOptStat("e")
    gStyle.SetStatBorderSize(0);

def labelsandstyle1d(h=None,XLabel=None,YLabel=None):
    
    h.GetXaxis().SetTitle(XLabel)
    h.GetYaxis().SetTitle(YLabel)
    h.GetXaxis().SetTitleSize(0.045)
    h.GetYaxis().SetTitleSize(0.045)

    h.SetLineColor(kBlack)
    h.SetFillColor(kBlue)

    caption=ROOT.TLatex()
    caption.SetTextSize(0.045)
    caption.SetTextFont(42)
    caption.SetNDC()
    caption.DrawLatex(0.1,0.91,'QIE10 Chip Test')


def labelsandstyle2d(h=None,hx=None,hy=None,XLabel=None,YLabel=None):

    h.SetXTitle(XLabel)
    h.GetYaxis().SetTitleOffset(1)
    h.SetYTitle(YLabel)
    h.GetXaxis().SetTitleSize(0.045)
    h.GetYaxis().SetTitleSize(0.045)
    h.SetMarkerColor(4)
    h.SetTitle('QIE10 Test: %s vs %s'%(hy,hx))

def draw1dplot(filename=None,h=None,Locut=None,Hicut=None,XLabel=None,YLabel=None,nbins=None):

    # Open the root file
    f,t=openfile(filename=filename)

    #Get info for the histogram based on a quick draw and removing the chips that are not working well using some cuts
    htemp = TH1F()
    t.Draw(h,"(IDCset0a < 1.21) && (ImpDiff_RinSel0 < 0.0048) &&  (SumDAC4 > 1200) && (Int_R0S0_CID3 < 60) && (Int_R1S1_CID0 < 225) && (Int_R2S1_CID0 < 2500)  && (Int_R3S1_CID0 < 18000) && (Int_R1S1_CID0 < 600) && (Slope_R1S0_CID0 < 30) && (Slope_R2S0_CID2 < 400) && (Slope_R2S1_CID0 < 425)" )
    htemp = gPad.GetPrimitive("htemp")
    mn = htemp.GetXaxis().GetXmin()
    mx = htemp.GetXaxis().GetXmax()
    bins=int(nbins)
   

    #If your histograms are ADCDNL, Sum4DNL or TDCVertOffset they are treated in a different way because of their entries.
    if h == 'ADCDNL':	
     h1d=TH1F()
     h1d=htemp.Clone()
    elif h == 'Sum4DNL':
     h1d=TH1F()
     h1d=htemp.Clone()
    elif h =='TDCVertOffset':
     h1d=TH1F()
     h1d=htemp.Clone()

    else:

     #Fill your histograms
     h1d = TH1F("h1d",h,bins,mn,mx)  
     nentry = t.GetEntries()  	
     for i in range(0,nentry):
         t.GetEntry(i)
         var=getattr(t,"%s"%h) 
         h1d.Fill(var) 

     # Plot statistics using a different style
     stats1d()	 

    #Create a canvas for your plot
    c1 = TCanvas("c1","c1")

    #Draw the histogram
    h1d.Draw()

    #Draw cut bars in the histograms in the same canvas
    ymax = h1d.GetMaximum()
    xmin = h1d.GetXaxis().GetXmin()
    xmax = h1d.GetXaxis().GetXmax()

    ##Draw or not the Low cut bar
    if not Locut == -999999:
        Cut1 = TLine(Locut, 0,Locut, ymax)
        Cut1.SetLineColor(2)
        Cut1.SetLineWidth(2)
        if  xmin <= Locut <= xmax:
           Cut1.Draw("same")
        else:
           caption1 = ROOT.TLatex()
           caption1.SetTextSize(0.039)
           caption1.SetTextFont(42)
           caption1.SetNDC()
           caption1.DrawLatex(0.30,0.84,'LoCut out of the range')

    ##Draw or not the Hi cut bar
    if not Hicut == -999999:
        Cut2 = TLine(Hicut, 0, Hicut, ymax)
        Cut2.SetLineColor(2)
        Cut2.SetLineWidth(2)
        if xmin <= Hicut <= xmax:
           Cut2.Draw("same")
        else:
           caption2=ROOT.TLatex()
           caption2.SetTextSize(0.039)
           caption2.SetTextFont(42)
           caption2.SetNDC()
           caption2.DrawLatex(0.30,0.80,'HiCut out of the range')

    ##Edit the labels and histogram the way you want
    labelsandstyle1d(h=h1d,XLabel=XLabel,YLabel=YLabel)
 
    ##save and delete
    c1.SaveAs( h + '.pdf' )
    del c1

def draw2dplot(filename=None,hx=None,hy=None,hxLabel=None,hyLabel=None):

    #Open the root file
    f,t=openfile(filename=filename)
    h2d =TH2F()

    # Plot statistics using a different style
    stats2d()
 
    #Create a canvas for your plots    
    c2 = TCanvas("c2","c2")

    ##Draw the TH2D
    t.Draw('%s:%s>>h'%(hy,hx),'','scat')
    h2d = gPad.GetListOfPrimitives().FindObject("h")

    ##Edit the labels and histogram the way you want
    labelsandstyle2d(h=h2d,hx=hx,hy=hy,XLabel=hxLabel,YLabel=hyLabel)

    ##Save and delete
    c2.SaveAs(hy +'_VS_'+ hx + '.pdf')
    del c2

def saveplots(directoryname=None):
    
    os.system("mkdir %s"%(directoryname))
    os.system("cp *.pdf ./%s"%(directoryname))
    os.system("rm *.pdf")
       
def main(argv=None):

    #Run the plotter
    th1f,cutbars,th2f,filename=runPlotter()

    #Open text files with information for the plots and make their respective arrays
    histograms = numpy.loadtxt('qie10_histos.txt', dtype='string')
    bins = numpy.loadtxt('qie10_bins.txt', dtype=int)
    cuts = numpy.loadtxt('qie10_cuts.txt', dtype=float)
    labels = numpy.loadtxt('qie10_labels.txt', dtype='string')

    #Start to plot all over the TH1F-histograms (qie10_histos.txt)
    if th1f == 'Yes':
   
       nh = len(histograms)

       #Make a loop over all the histograms
       for i in range(0,nh):
           #Get the variables for  h,Locut,Hicut,Xunit,Yunits from the arrays
             histoname = histograms[i]
             numbins = bins[i]
             Xunits = labels[i,0]
             Yunits = labels[i,1]   
             locut = cuts[i,0]
             hicut = cuts[i,1]

             #Here is when it's decided to add or not the cut bars in the plots                         
             if cutbars == 'Yes': draw1dplot(filename=filename,h=histoname,Locut=locut,Hicut=hicut,XLabel=Xunits,YLabel=Yunits,nbins=numbins)  
             if cutbars == 'No': draw1dplot(filename=filename,h=histoname,Locut=-999999,Hicut=-999999,XLabel=Xunits,YLabel=Yunits,nbins=numbins)

       #Save 1d-plots 
       saveplots(directoryname='qie10plots')

    #Start to plot all over the TH2F-histograms (qie10_2dhistos.txt)
    if th2f == 'Yes':

       #Open text file with 2d-plot name of the histograms         
       histograms2d = numpy.loadtxt('qie10_2dhistos.txt', dtype='string')
       n2h = len(histograms2d)
 
       #Make a loop all over the 2d 
       for j in range(0,n2h):
             #Get the names for histo1, histo2
             histx = histograms2d[j,0]
             histy = histograms2d[j,1]

             #Get the labels for histo1, histo2             
             ix = histograms.tolist().index(histx) 
       	     iy	= histograms.tolist().index(histy)
             hxunits = labels[ix,0]
             hyunits = labels[iy,0]

             #Draw the 2d-plot
             draw2dplot(filename=filename,hx=histx,hy=histy,hxLabel=hxunits,hyLabel=hyunits)

       #Save 2d-plots
       saveplots(directoryname='qie10plots2dscat')
 
if __name__ == "__main__":
    sys.exit(main())

