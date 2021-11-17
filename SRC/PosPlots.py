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

    PlotConf["Title"] = "%s for PA from %s on Year %s"\
        " DoY %s" % (Title, Rcvr, Year, Doy)

    PlotConf["Path"] = sys.argv[1] + '/OUT/SPVT/Figures/%s/' % Label + \
        '%s_%s_Y%sD%s.png' % (Label, Rcvr, Year, Doy)

# Plot DOPS
def plotDops(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "DOPS", "DOPS_vs_TIME")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (10.4,7.6)
    PlotConf["SecondAxis"] = ["Num SV PA"]

    PlotConf["yLabel"] = "DOP [m]"
    PlotConf["y2Label"] = "Number of satellites used for PA solution"

    PlotConf["y2Lim"] = [0,max(sorted(PosData[PosIdx["NVS-SOL"]])) + 1]

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = ["HDOP","VDOP","PDOP","TDOP","Num SV PA"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    FilterCond = PosData[PosIdx["SOL"]] == 1
    for Label in PlotConf["Legend"]:
        if Label == "Num SV PA":
            PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
            PlotConf["yData"][Label] = PosData[PosIdx["NVS-SOL"]][FilterCond]
        else:
            PlotConf["xData"][Label] = PosData[PosIdx["SOD"]] / GnssConstants.S_IN_H
            PlotConf["yData"][Label] = PosData[PosIdx[Label]]

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Position Errors vs Position Limits
def plotErrorVsLimit(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "PE vs PL", "POS_ERROR_vs_LIMIT")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (10.4,7.6)

    PlotConf["yLabel"] = "Value [m]"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = ["VPE","HPE","HPL","VPL"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    FilterCond = PosData[PosIdx["SOL"]] == 1
    for Label in PlotConf["Legend"]:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = abs(PosData[PosIdx[Label]][FilterCond].to_numpy())

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Position Errors
def plotErrors(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Position Errors", "POS_ERROR_vs_TIME")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (10.4,7.6)

    PlotConf["yLabel"] = "Position Errors [m]"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["Legend"] = ["VPE","HPE"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    FilterCond = PosData[PosIdx["SOL"]] == 1
    for Label in PlotConf["Legend"]:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = PosData[PosIdx[Label]][FilterCond]

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot HPE vs HDOP
def plotHorizontalPE(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "HPE vs DOP", "HPE_vs_HDOP")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,7.6)

    PlotConf["xLabel"] = "EPE [m]"
    PlotConf["yLabel"] = "NPE [m]"

    PlotConf["Grid"] = True

    PlotConf["Marker"] = '+'
    PlotConf["LineWidth"] = 0.75

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
def plotSafeIndex(PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Safety Index", "SAFE_INDEX_vs_TIME")

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (10.4,7.6)

    PlotConf["yLabel"] = "Safety Index"

    PlotConf["xTicks"] = range(0,25)
    PlotConf["xLim"] = [0,24]

    PlotConf["Grid"] = True
    PlotConf["HLine"] = [(1.0, 0, 24)]
    PlotConf["Legend"] = ["VSI","HSI"]

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    # Plotting
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    FilterCond = PosData[PosIdx["SOL"]] == 1
    for Label in PlotConf["Legend"]:
        PlotConf["xData"][Label] = PosData[PosIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = abs(PosData[PosIdx[Label]][FilterCond].to_numpy())

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Horizontal Standford Diagram
def plotHorStand(Conf, PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Horizontal Standford Diagram", "HOR_STANDFORD_DIAGRAM")

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

# Plot Vertical Standford Diagram
def plotVerStand(Conf, PosFile, PosData):

    # Graph settings definition
    PlotConf = {}
    initPlot(PosFile, PlotConf, "Vertical Standford Diagram", "VER_STANDFORD_DIAGRAM")

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
    usecols=[PosIdx["SOD"],PosIdx["NVS-SOL"],PosIdx["HDOP"],PosIdx["VDOP"],PosIdx["PDOP"],PosIdx["TDOP"],PosIdx["SOL"]])

    print( 'Plot DOPS vs Time for PA...')
    
    # Configure plot and call plot generation function
    plotDops(PosFile, PosData)

    # POSITION ERRORS VS POSITION LIMITS
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HPE"],PosIdx["VPE"],PosIdx["HPL"],PosIdx["VPL"],PosIdx["SOL"]])

    print( 'Plot Position Errors vs Position Limits vs Time for PA...')
    
    # Configure plot and call plot generation function
    plotErrorVsLimit(PosFile, PosData)

    # POSITION ERRORS vs TIME
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HPE"],PosIdx["VPE"],PosIdx["SOL"]])

    print( 'Plot Position Errors vs Time for PA...')
    
    # Configure plot and call plot generation function
    plotErrors(PosFile, PosData)

    # HORIZONTAL POSITION ERROR vs HDOP
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["EPE"],PosIdx["NPE"],PosIdx["HDOP"],PosIdx["SOL"]])

    print( 'Plot Horizontal Position Error vs HDOP for PA...')
    
    # Configure plot and call plot generation function
    plotHorizontalPE(PosFile, PosData)

    # SAFETY INDEX vs TIME
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["SOD"],PosIdx["HSI"],PosIdx["VSI"],PosIdx["SOL"]])

    print( 'Plot Safety Index vs Time for PA...')
    
    # Configure plot and call plot generation function
    plotSafeIndex(PosFile, PosData)

    # HORIZONTAL STANDFORD DIAGRAM
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["HPE"],PosIdx["HPL"],PosIdx["SOL"]])

    print( 'Plot Horizontal Standford Diagram for PA...')
    
    # Configure plot and call plot generation function
    plotHorStand(Conf, PosFile, PosData)

    # VERTICAL STANDFORD DIAGRAM
    # ----------------------------------------------------------
    # Read the cols we need from PosFile file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PosIdx["VPE"],PosIdx["VPL"],PosIdx["SOL"]])

    print( 'Plot Vertical Standford Diagram for PA...')
    
    # Configure plot and call plot generation function
    plotVerStand(Conf, PosFile, PosData)