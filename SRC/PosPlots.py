#!/usr/bin/env python

########################################################################
# PETRUS/SRC/PosPlots.py:
# This is the PosPlots Module of PETRUS tool
#
#  Project:        PETRUS
#  File:           PosPlots.py
#  Date(YY/MM/DD): 10/17/21
#
#   Author: GNSS Academy
#   Copyright 2021 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
########################################################################

import sys, os
from pandas import read_csv
from InputOutput import PosIdx
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
from COMMON.Plots import generatePlot
import numpy as np
from scipy.stats import gaussian_kde

def initPlot(PosFile, PlotConf, Title, Label):
    
    # Compute information from PosFile
    PosFileName = os.path.basename(PosFile)
    PosFileNameSplit = PosFileName.split('_')
    Rcvr = PosFileNameSplit[1]
    DatepDat = PosFileNameSplit[2]
    Date = DatepDat.split('.')[0]
    Year = Date[1:3]
    Doy = Date[4:]

    # Dump information into PlotConf
    PlotConf["xLabel"] = "Hour of Day %s" % Doy

    PlotConf["Title"] = "%s from %s on Year %s"\
        " DoY %s" % (Title, Rcvr, Year, Doy)

    PlotConf["Path"] = sys.argv[1] + '/OUT/SPVT/Figures/%s/' % Label + \
        '%s_%s_Y%sD%s.png' % (Label, Rcvr, Year, Doy)

# Plot DOP
def plotDop(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "DOP", "DOP")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.4,7.6)
    PlotConf["SecondAxis"] = ["Num SV PA"]

    PlotConf["y1Label"] = "DOP [m]"
    PlotConf["y2Label"] = "Number of satellites used for PA solution"

    PlotConf["y1Lim"] = [0, 5]
    PlotConf["y2Lim"] = [0,max(sorted(PosData[PosIdx["NSV-SOL"]])) + 1]

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = True
    PlotConf["DoubleAxis"] = True

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    Label = ["TDOP","PDOP","VDOP","HDOP","Num SV PA"]

    PlotConf["xData"] = {}
    PlotConf["y1Data"] = {}
    PlotConf["y2Data"] = {}
    PlotConf["Color"] = {}

    FilterCond = PosData[PosIdx["SOL"]] == 1

    for Label in Label:
        if Label == "Num SV PA":
            PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
            PlotConf["y2Data"][Label] = PosData[PosIdx["NSV-SOL"]][FilterCond]
            PlotConf["Color"][Label] = 'orange'
        else:
            PlotConf["xData"][Label] = PosData[PosIdx["SOD"]] / GnssConstants.S_IN_H
            PlotConf["y1Data"][Label] = PosData[PosIdx[Label]]
        
            if Label == "TDOP":
                PlotConf["Color"][Label] = 'grey'
            elif Label == "PDOP":
                PlotConf["Color"][Label] = 'blue'
            elif Label == "VDOP":
                PlotConf["Color"][Label] = 'seagreen'
            elif Label == "HDOP":
                PlotConf["Color"][Label] = 'skyblue'
            else:  
                pass

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot PE vs PL
def plotPEvsPL(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "PE vs PL", "PE_vs_PL")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.4,7.6)

    PlotConf["yLabel"] = "Value [m]"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = True
    Label = ["VPE","VPL","HPE","HPL"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}
    
    FilterCond = PosData[PosIdx["SOL"]] == 1

    for Label in Label:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = abs(PosData[PosIdx[Label]][FilterCond].to_numpy())

        if Label == "VPE":
            PlotConf["Color"][Label] = 'seagreen'
        elif Label == "VPL":
            PlotConf["Color"][Label] = 'blue'
        elif Label == "HPE":
            PlotConf["Color"][Label] = 'darkred'
        elif Label == "HPL":
            PlotConf["Color"][Label] = 'orange'
        else:  
            pass

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot PE
def plotPE(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Position Errors", "PE")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.4,7.6)

    PlotConf["yLabel"] = "Position Errors [m]"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = True
    Label = ["VPE","HPE"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    FilterCond = PosData[PosIdx["SOL"]] == 1

    for Label in Label:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = PosData[PosIdx[Label]][FilterCond]

        if Label == "VPE":
            PlotConf["Color"][Label] = 'seagreen'
        else:
            PlotConf["Color"][Label] = 'darkred'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot HPE vs HDOP
def plotHPE(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "HPE vs DOP", "HPE_vs_DOP")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (10.4,7.6)

    PlotConf["xLabel"] = "EPE [m]"
    PlotConf["yLabel"] = "NPE [m]"

    PlotConf["Grid"] = True

    PlotConf["Marker"] = 'o'
    PlotConf["LineWidth"] = 0.75
    PlotConf["Alpha"] = 0.75

    # Colorbar definition
    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "HDOP"
    PlotConf["ColorBarMin"] = min(sorted(PosData[PosIdx["HDOP"]]))
    PlotConf["ColorBarMax"] = max(sorted(PosData[PosIdx["HDOP"]]))

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    FilterCond = PosData[PosIdx["SOL"]] == 1

    Label = 0
    PlotConf["xData"][Label] = PosData[PosIdx["EPE"]][FilterCond]
    PlotConf["yData"][Label] = PosData[PosIdx["NPE"]][FilterCond]
    PlotConf["zData"][Label] = PosData[PosIdx["HDOP"]][FilterCond]

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Safety Index
def plotSI(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Safety Index", "SI")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.4,7.6)

    PlotConf["yLabel"] = "Safety Index"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["HLine"] = [(1.0, 0, 24)]
    PlotConf["Legend"] = True
    Label = ["VSI","HSI"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    FilterCond = PosData[PosIdx["SOL"]] == 1

    for Label in Label:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = abs(PosData[PosIdx[Label]][FilterCond].to_numpy())

        if Label == "VSI":
            PlotConf["Color"][Label] = 'seagreen'
        else:
            PlotConf["Color"][Label] = 'darkred'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Horizontal Stanford Diagram
def plotHStanford(Conf, PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Horizontal Stanford Diagram", "HOR_STANFORD_DIAGRAM")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,7.6)

    PlotConf["xLabel"] = "HPE [m]"
    PlotConf["yLabel"] = "HPL [m]"

    PlotConf["xLim"] = [0,50]
    PlotConf["yLim"] = [0,50]
    PlotConf["HLine"] = [(Conf["LPV200"][1], 0, 50), (Conf["APVI"][1], 0, 50)]
    PlotConf["VLine"] = [(Conf["LPV200"][1], 0, 50), (Conf["APVI"][1], 0, 50)]
    PlotConf["SLine"] = [np.array([0,50]), np.array([0,50])]

    PlotConf["Grid"] = True
    
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Processing data to be plotted
    FilterCond = PosData[PosIdx["SOL"]] == 1

    Hpe = PosData[PosIdx["HPE"]][FilterCond].to_numpy()
    Hpl = PosData[PosIdx["HPL"]][FilterCond].to_numpy()
    # Get point density data
    Den = np.vstack([Hpe,Hpl])
    ZData = gaussian_kde(Den)(Den)
    # Sort data by point density values
    idx = ZData.argsort()
    Hpe, Hpl, ZData = Hpe[idx], Hpl[idx], ZData[idx]

    # Colorbar definition
    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Point Density (Number of Samples : " + str(len(Hpe)) + ")"
    PlotConf["ColorBarMin"] = min(ZData)
    PlotConf["ColorBarMax"] = max(ZData)

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    Label = 0
    PlotConf["xData"][Label] = Hpe
    PlotConf["yData"][Label] = Hpl
    PlotConf["zData"][Label] = ZData

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Vertical Stanford Diagram
def plotVStanford(Conf, PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Vertical Stanford Diagram", "VER_STANFORD_DIAGRAM")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,7.6)

    PlotConf["xLabel"] = "VPE [m]"
    PlotConf["yLabel"] = "VPL [m]"

    PlotConf["xLim"] = [0,60]
    PlotConf["yLim"] = [0,60]
    PlotConf["HLine"] = [(Conf["LPV200"][2], 0, 60), (Conf["APVI"][2], 0, 60)]
    PlotConf["VLine"] = [(Conf["LPV200"][2], 0, 60), (Conf["APVI"][2], 0, 60)]
    PlotConf["SLine"] = [np.array([0,60]), np.array([0,60])]

    PlotConf["Grid"] = True
    
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Processing data to be plotted
    FilterCond = PosData[PosIdx["SOL"]] == 1

    Vpe = PosData[PosIdx["VPE"]][FilterCond].to_numpy()
    Vpl = PosData[PosIdx["VPL"]][FilterCond].to_numpy()
    # Get point density data
    Den = np.vstack([Vpe,Vpl])
    ZData = gaussian_kde(Den)(Den)
    # Sort data by point density values
    idx = ZData.argsort()
    Vpe, Vpl, ZData = Vpe[idx], Vpl[idx], ZData[idx]

    # Colorbar definition
    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Point Density (Number of Samples : " + str(len(Vpe)) + ")"
    PlotConf["ColorBarMin"] = min(ZData)
    PlotConf["ColorBarMax"] = max(ZData)

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    Label = 0
    PlotConf["xData"][Label] = abs(Vpe)
    PlotConf["yData"][Label] = Vpl
    PlotConf["zData"][Label] = ZData

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

def generatePosPlots(Conf, PosFile):
    
    # Purpose: generate output plots regarding svpt results

    # Parameters
    # ==========
    # Conf: dict
    #       Configuration dictionary
    # PosFile: str
    #          Path to POS output file

    # Returns
    # =======
    # Nothing

    # ----------------------------------------------------------
    # PLOTTING FUNCTIONS
    # ----------------------------------------------------------

    # DOPS vs TIME
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["NSV-SOL"],PosIdx["HDOP"],PosIdx["VDOP"],PosIdx["PDOP"],PosIdx["TDOP"],PosIdx["SOL"]])

    print( 'Plot Dilution Of Precision vs Time...')
    
    # Configure plot and call plot generation function
    plotDop(PosFile, PosData)

    # POSITION ERRORS VS POSITION LIMITS
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HPE"],PosIdx["VPE"],PosIdx["HPL"],PosIdx["VPL"],PosIdx["SOL"]])

    print( 'Plot Position Errors vs Position Limits vs Time...')
    
    # Configure plot and call plot generation function
    plotPEvsPL(PosFile, PosData)

    # POSITION ERRORS vs TIME
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HPE"],PosIdx["VPE"],PosIdx["SOL"]])

    print( 'Plot Position Errors vs Time...')
    
    # Configure plot and call plot generation function
    plotPE(PosFile, PosData)

    # HORIZONTAL POSITION ERROR vs HDOP
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["EPE"],PosIdx["NPE"],PosIdx["HDOP"],PosIdx["SOL"]])

    print( 'Plot Horizontal Position Error vs Horizontal Dilution Of Precision...')
    
    # Configure plot and call plot generation function
    plotHPE(PosFile, PosData)

    # SAFETY INDEX vs TIME
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HSI"],PosIdx["VSI"],PosIdx["SOL"]])

    print( 'Plot Safety Index vs Time...')
    
    # Configure plot and call plot generation function
    plotSI(PosFile, PosData)

    # HORIZONTAL STANFORD DIAGRAM
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["HPE"],PosIdx["HPL"],PosIdx["SOL"]])

    print( 'Plot Horizontal Stanford Diagram...')
    
    # Configure plot and call plot generation function
    plotHStanford(Conf, PosFile, PosData)

    # VERTICAL STANFORD DIAGRAM
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["VPE"],PosIdx["VPL"],PosIdx["SOL"]])

    print( 'Plot Vertical Stanford Diagram...')
    
    # Configure plot and call plot generation function
    plotVStanford(Conf, PosFile, PosData)