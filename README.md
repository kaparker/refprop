# Refprop Analysis code

Basic CO2 analysis using temperatures 1-10 and pressure measurements p1, p2 to calculate the saturation properties.
Note, units of input data: pressure [bar], temperature [C].

Use pyROOT to make 4 histograms:
1.) abs(pressure - satpressure) vs. time
2.) abs(temp - sattemp) vs. time
3.) raw temp 1-10, sattemp 1,2 vs. time
4.) raw pressure 1,2, satpress 1-10 vs. time
5.) raw pressure 1,2 satpress 1,2,9,10 vs. time
6.) raw temp 1,2,9,10, sattemp 1,2 vs. time
