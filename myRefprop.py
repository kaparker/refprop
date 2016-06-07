# -*- coding: utf-8 -*-
"""
Created on Wed June 1 2016
@author: parker
Edited from myRefProp.py
"""
from pyrp.refpropClasses import *
import ROOT
import numpy
from pyrp.refpropClasses import RefpropSI 
RP = RefpropSI()
RP.fpath = "/home/parker/.refprop/"
RP.SETPATH(RP.fpath)
RP.SETUP('CO2.FLD')

filein="/home/parker/Refprop/raw_data/22-08-cooldown.txt"
# Temp in C, Press in bar
#filein="22-08-cooldown.txt"
inF=open(filein,'r')
read_line=0
temp1=[]
temp2=[]
temp3=[]
temp4=[]
temp5=[]
temp6=[]
temp7=[]
temp8=[]
temp9=[]
temp10=[]
press1=[]
press2=[]
satpress1=[]
satpress2=[]
satpress1a=[]
satpress2a=[]
satpress1avg=[]
satpress2avg=[]
sattemp1=[]
sattemp2=[]
temp1avg=[]
temp2avg=[]
diff1=[]
diff2=[]
diff1a=[]
diff2a=[]
diff1avg=[]
diff2avg=[]
diff3=[]
diff4=[]
diff3a=[]
diff4a=[]
diff3avg=[]
diff4avg=[]

for line in inF:
    if (read_line>2):    
        myline=line.split()
        temp1.append(float(myline[2]))
        temp2.append(float(myline[3]))
        temp3.append(float(myline[4]))
        temp4.append(float(myline[5]))
        temp5.append(float(myline[6]))
        temp6.append(float(myline[7]))
        temp7.append(float(myline[8]))
        temp8.append(float(myline[9]))
        temp9.append(float(myline[10]))
        temp10.append(float(myline[11]))
        press1.append(float(myline[12])+float(myline[14]))
        press2.append(float(myline[13])+float(myline[14]))
    else:
        read_line+=1

for i in range(len(temp1)):
    # get saturation pressure, convert to bar
    T,p_1,Dl,Dv = RP.SATT(abs(C(temp9[i])),kph=1) #the C-->K conversion happens inside
    T,p_1a,Dl,Dv = RP.SATT(abs(C(temp10[i])),kph=1) #the C-->K conversion happens inside
    T,p_2,Dl,Dv = RP.SATT(abs(C(temp1[i])),kph=1) #the C-->K conversion happens inside
    T,p_2a,Dl,Dv = RP.SATT(abs(C(temp2[i])),kph=1) #the C-->K conversion happens inside
    T_1,p,Dl,Dv = RP.SATP(abs(bar(press1[i])),kph=1)
    T_2,p,Dl,Dv = RP.SATP(abs(bar(press2[i])),kph=1)
    
     #print Pa(p_1)
     #print Pa(p_2)

    satpress1.append(Pa(p_1)) #passing Pa to become bar
    satpress2.append(Pa(p_2)) #passing Pa to become bar
    satpress1a.append(Pa(p_1a)) #passing Pa to become bar
    satpress2a.append(Pa(p_2a)) #passing Pa to become bar
    sattemp1.append(K(T_1)) # passing K to become C
    sattemp2.append(K(T_2)) # passing K to become C
    
    diff1.append(abs(press1[i]-satpress1[i]))
    diff2.append(abs(press2[i]-satpress2[i]))
    diff1a.append(abs(press1[i]-satpress1a[i]))
    diff2a.append(abs(press2[i]-satpress2a[i]))
    
    satpress1avg.append((satpress1[i]+satpress1a[i])/2)
    satpress2avg.append((satpress2[i]+satpress2a[i])/2)
    diff1avg.append(abs(press1[i]-satpress1avg[i]))
    diff2avg.append(abs(press2[i]-satpress2avg[i]))

    diff3.append(abs(temp9[i]-sattemp1[i]))
    diff4.append(abs(temp1[i]-sattemp2[i]))
    diff3a.append(abs(temp10[i]-sattemp1[i]))
    diff4a.append(abs(temp2[i]-sattemp2[i]))

    temp1avg.append((temp9[i]+temp10[i])/2)
    temp2avg.append((temp1[i]+temp2[i])/2)
    diff3avg.append(abs(temp1avg[i]-sattemp1[i]))
    diff4avg.append(abs(temp2avg[i]-sattemp2[i]))

time=[float(x) for x in range(0,len(diff1))]

x=numpy.array(time)
y=numpy.array(diff1)
z=numpy.array(diff2)
ya=numpy.array(diff1a)
za=numpy.array(diff2a)
yavg=numpy.array(diff1avg)
zavg=numpy.array(diff2avg)

A=numpy.array(diff3)
B=numpy.array(diff4)
Aa=numpy.array(diff3a)
Ba=numpy.array(diff4a)
Aavg=numpy.array(diff3avg)
Bavg=numpy.array(diff4avg)


mg = ROOT.TMultiGraph()
canv = ROOT.TCanvas("canv","",600,600)
gr1 = ROOT.TGraph(len(x), x,y )
gr2 = ROOT.TGraph(len(x), x,z )
gr1a = ROOT.TGraph(len(x), x,ya )
gr2a = ROOT.TGraph(len(x), x,za )
gr1avg = ROOT.TGraph(len(x), x,yavg )
gr2avg = ROOT.TGraph(len(x), x,zavg )

gr1.SetMarkerStyle(21);
gr1.SetMarkerColor(3);
gr1.SetMarkerSize(1);
gr2.SetMarkerStyle(22);
gr2.SetMarkerColor(4);
gr2.SetMarkerSize(1);
gr1a.SetMarkerStyle(21);
gr1a.SetMarkerColor(2);
gr1a.SetMarkerSize(1);
gr2a.SetMarkerStyle(22);
gr2a.SetMarkerColor(5);
gr2a.SetMarkerSize(1);
gr1avg.SetMarkerStyle(21);
gr1avg.SetMarkerColor(1);
gr1avg.SetMarkerSize(0.2);
gr2avg.SetMarkerStyle(22);
gr2avg.SetMarkerColor(1);
gr2avg.SetMarkerSize(0.5);

mg.Add(gr1,"p")
mg.Add(gr2,"p")
mg.Add(gr1a,"p")
mg.Add(gr2a,"p")
mg.Add(gr1avg,"p")
mg.Add(gr2avg,"p")
mg.Draw("ap")
h1=mg.GetHistogram()
h1.GetYaxis().SetTitle("|pr - SATT| [bar]")
h1.GetXaxis().SetTitle("Time [sec]")
h1.Draw("samep noaxis")

legend=ROOT.TLegend(0.8,0.8,0.95,0.95)
legend.AddEntry(gr1, "p1 t9", "p")
legend.AddEntry(gr2, "p2 t1", "p")
legend.AddEntry(gr1a, "p1 t10", "p")
legend.AddEntry(gr2a, "p2 t2", "p")
legend.AddEntry(gr1avg, "p1 tavg", "p")
legend.AddEntry(gr2avg, "p2 tavg", "p")
legend.SetBorderSize(0);
legend.SetFillColor(0);
legend.Draw()

canv.Print("press_sattemp_sensor.png")

mg2 = ROOT.TMultiGraph()
canv2 = ROOT.TCanvas("canv2","",600,600)
gr3 = ROOT.TGraph(len(x), x,A )
gr4 = ROOT.TGraph(len(x), x,B )
gr3a = ROOT.TGraph(len(x), x,Aa )
gr4a = ROOT.TGraph(len(x), x,Ba )
gr3avg = ROOT.TGraph(len(x), x,Aavg )
gr4avg = ROOT.TGraph(len(x), x,Bavg )

gr3.SetMarkerStyle(21);
gr3.SetMarkerColor(3);
gr3.SetMarkerSize(1);
gr4.SetMarkerStyle(22);
gr4.SetMarkerColor(4);
gr4.SetMarkerSize(1);
gr3a.SetMarkerStyle(21);
gr3a.SetMarkerColor(2);
gr3a.SetMarkerSize(1);
gr4a.SetMarkerStyle(22);
gr4a.SetMarkerColor(5);
gr4a.SetMarkerSize(1);
gr3avg.SetMarkerStyle(21);
gr3avg.SetMarkerColor(1);
gr3avg.SetMarkerSize(0.2);
gr4avg.SetMarkerStyle(22);
gr4avg.SetMarkerColor(1);
gr4avg.SetMarkerSize(0.5);

mg2.Add(gr3,"p")
mg2.Add(gr4,"p")
mg2.Add(gr3a,"p")
mg2.Add(gr4a,"p")
mg2.Add(gr3avg,"p")
mg2.Add(gr4avg,"p")
mg2.Draw("ap")
h2=mg2.GetHistogram()
h2.GetYaxis().SetTitle("|T - SATP| [C]")
h2.GetXaxis().SetTitle("Time [sec]")
h2.Draw("samep noaxis")

legend2=ROOT.TLegend(0.8,0.8,0.95,0.95)
legend2.AddEntry(gr3, "p1 t9", "p")
legend2.AddEntry(gr4, "p2 t1", "p")
legend2.AddEntry(gr3a, "p1 t10", "p")
legend2.AddEntry(gr4a, "p2 t2", "p")
legend2.AddEntry(gr3avg, "p1 tavg", "p")
legend2.AddEntry(gr4avg, "p2 tavg", "p")
legend2.SetBorderSize(0);
legend2.SetFillColor(0);
legend2.Draw()

canv2.Print("satpress_temp_sensor.png")

t1=numpy.array(temp1)
t2=numpy.array(temp2)
t3=numpy.array(temp3)
t4=numpy.array(temp4)
t5=numpy.array(temp5)
t6=numpy.array(temp6)
t7=numpy.array(temp7)
t8=numpy.array(temp8)
t9=numpy.array(temp9)
t10=numpy.array(temp10)
p1=numpy.array(press1)
p2=numpy.array(press2)
tp1=numpy.array(sattemp1)
tp2=numpy.array(sattemp2)

mg3 = ROOT.TMultiGraph()
canv3 = ROOT.TCanvas("canv3","",600,600)
grT1 = ROOT.TGraph(len(x), x,t1 )
grT2 = ROOT.TGraph(len(x), x,t2 )
grT3 = ROOT.TGraph(len(x), x,t3 )
grT4 = ROOT.TGraph(len(x), x,t4 )
grT5= ROOT.TGraph(len(x), x,t5 )
grT6 = ROOT.TGraph(len(x), x,t6 )
grT7 = ROOT.TGraph(len(x), x,t7 )
grT8 = ROOT.TGraph(len(x), x,t8 )
grT9 = ROOT.TGraph(len(x), x,t9 )
grT10 = ROOT.TGraph(len(x), x,t10 )
grTP1 = ROOT.TGraph(len(x), x,tp1 )
grTP2 = ROOT.TGraph(len(x), x,tp2 )

grT9.SetMarkerStyle(21);
grT9.SetMarkerColor(3);
grT9.SetMarkerSize(1);
grT1.SetMarkerStyle(22);
grT1.SetMarkerColor(4);
grT1.SetMarkerSize(1);
grT10.SetMarkerStyle(21);
grT10.SetMarkerColor(2);
grT10.SetMarkerSize(1);
grT2.SetMarkerStyle(22);
grT2.SetMarkerColor(5);
grT2.SetMarkerSize(1);
grTP1.SetMarkerStyle(21);
grTP1.SetMarkerColor(1);
grTP1.SetMarkerSize(1);
grTP2.SetMarkerStyle(22);
grTP2.SetMarkerColor(12);
grTP2.SetMarkerSize(1);
grT3.SetMarkerStyle(21);
grT3.SetMarkerColor(6);
grT3.SetMarkerSize(1);
grT4.SetMarkerStyle(22);
grT4.SetMarkerColor(7);
grT4.SetMarkerSize(1);
grT5.SetMarkerStyle(21);
grT5.SetMarkerColor(8);
grT5.SetMarkerSize(1);
grT6.SetMarkerStyle(22);
grT6.SetMarkerColor(9);
grT6.SetMarkerSize(1);
grT7.SetMarkerStyle(21);
grT7.SetMarkerColor(10);
grT7.SetMarkerSize(1);
grT8.SetMarkerStyle(22);
grT8.SetMarkerColor(11);
grT8.SetMarkerSize(1);

mg3.Add(grT1,"p")
mg3.Add(grT2,"p")
mg3.Add(grT3,"p")
mg3.Add(grT4,"p")
mg3.Add(grT5,"p")
mg3.Add(grT6,"p")
mg3.Add(grT7,"p")
mg3.Add(grT8,"p")
mg3.Add(grT9,"p")
mg3.Add(grT10,"p")
mg3.Add(grTP1,"p")
mg3.Add(grTP2,"p")
mg3.Draw("ap")

h3=mg3.GetHistogram()
h3.GetYaxis().SetTitle("Temperature [C]")
h3.GetXaxis().SetTitle("Time [sec]")
h3.Draw("samep noaxis")
legend3=ROOT.TLegend(0.8,0.7,0.95,0.95)
legend3.AddEntry(grT1, "T1", "p")
legend3.AddEntry(grT2, "T2", "p")
legend3.AddEntry(grT3, "T3", "p")
legend3.AddEntry(grT4, "T4", "p")
legend3.AddEntry(grT5, "T5", "p")
legend3.AddEntry(grT6, "T6", "p")
legend3.AddEntry(grT7, "T7", "p")
legend3.AddEntry(grT8, "T8", "p")
legend3.AddEntry(grT9, "T9", "p")
legend3.AddEntry(grT10, "T10", "p")
legend3.AddEntry(grTP1, "SatP1", "p")
legend3.AddEntry(grTP2, "SatP2", "p")
legend3.SetBorderSize(0);
legend3.SetFillColor(0);
legend3.Draw()
canv3.Print("satpress_temp_all.png")

inF.close()
raw_input()
