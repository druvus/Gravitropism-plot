#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys, argparse
import math
import pylab
from pylab import *
import array
from numpy import *
import scipy

parser = argparse.ArgumentParser(description='This is a gravitropism plotting script by Andreas Sjödin.')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-T','--title',help='Output file prefix', required=True)
parser.add_argument('-s','--plotline',help='Plot seperator lines (T/F)', required=True)
args = parser.parse_args()


#Set fixed arguments
radie = 3
scaleup = 10

#Set command arguments
infile = args.input
datalabel = args.title
lineplotarg = args.plotline


if lineplotarg == 'T' :
  lineplot = True
else :
  lineplot = False

#Open file
f=open(infile, 'r')

#Read and convert data
indata = f.readline()

tempdata = indata.split()
tempdata2 = list()

for i in tempdata:
  tempdata2.append(float(i))

degreedata = tempdata2
arraydata = array(degreedata, 'f')

#Define bins
xydeg2 = array( [0, 30, 60 , 90, 120, 150, 180, 210, 240 , 270, 300, 330, 360], 'f' )

#Change coordinate system
xydeg = (xydeg2/360)*2*math.pi
xydeg = xydeg[1:]
xydeg = -xydeg
xylabel = array(xydeg2[1:], 'i')
xydeg = xydeg+(math.pi/12)

#Count inside each interval
histdata = hist(arraydata,xydeg2)[0]
mult = array(histdata, 'f')/sum(histdata)
ndir = len(mult)
smallDeg = (2*math.pi/ndir)/2

#Create array of numbers between 0 and 2*pi
deg = arange(0,2*math.pi,0.01)

#Plot circle
pylab.clf()

pylab.axis(xmin = -10, xmax=10, ymin=-10, ymax=10)
an = linspace(0,2*pi,100)
pylab.plot( radie*cos(an), radie*sin(an) , 'k')

#Fix degree label
xylabel[xylabel == 360] = 0

#Plot seperator lines
for i in range(ndir):
  if lineplot == True :  plot( [ (radie-0.4)*cos(xydeg[i]-smallDeg), (radie+0.4)*cos(xydeg[i]-smallDeg) ], [ (radie-0.4)*sin(xydeg[i]-smallDeg), (radie+0.4)*sin(xydeg[i]-smallDeg) ],'k')
  pylab.text( (radie*0.7)*cos(xydeg[i]-(pi/12)), (radie*0.7)*sin(xydeg[i]-(pi/12)), xylabel[i], ha = 'center' , va = 'center', size = 'small')
  if mult[i] != 0:
    pylab.plot( [ (radie+0.2)*cos(xydeg[i]), (radie)*cos(xydeg[i])+cos(xydeg[i])*scaleup*mult[i] ], [ (radie+0.2)*sin(xydeg[i]), (radie)*sin(xydeg[i])+sin(xydeg[i])*scaleup*mult[i] ] , 'k', linewidth = 15 )
    pylab.text( (1+radie)*cos(xydeg[i])+cos(xydeg[i])*scaleup*mult[i], (1+radie)*sin(xydeg[i])+sin(xydeg[i])*scaleup*mult[i], round(mult[i]*100) , color = 'r', ha = 'center' , va = 'center')

pylab.text(0,0, datalabel, ha = 'center', size = 'large')

#Plot title
#title(r'Gravitropism plot')
#pylab.frame.set_visble(False)

pylab.axis(xmin= -20, xmax=20, ymin= -20, ymax=20)
pylab.axis('scaled')
pylab.axis('off')
#ax.toggle_axisline(False)

pylab.savefig(datalabel+'.pdf')

#pylab.show()

