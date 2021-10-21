#!/usr/bin/env python

########################################################################
# PETRUS/SRC/Spvt.py:
# This is the Spvt Module of PETRUS tool
#
#  Project:        PETRUS
#  File:           Spvt.py
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


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON import GnssConstants as Const
from InputOutput import RcvrIdx, ObsIdx, CorrIdx, REJECTION_CAUSE
from InputOutput import FLAG, VALUE, TH, CSNEPOCHS
import numpy as np
from COMMON.Iono import computeIonoMappingFunction
from COMMON.Wlsq import wlsq

# Spvt internal functions
#-----------------------------------------------------------------------


def computeGRow(SatCorrInfo):

    x = - (np.cos(np.deg2rad(SatCorrInfo["Elevation"])) * np.sin(np.deg2rad(SatCorrInfo["Azimuth"])))
    y = - (np.cos(np.deg2rad(SatCorrInfo["Elevation"])) * np.cos(np.deg2rad(SatCorrInfo["Azimuth"])))
    z = - (np.sin(np.deg2rad(SatCorrInfo["Elevation"])))

    return [x, y, z, 1]


def computeDop(GMatrix, PosInfo):
    # Compute the DOP matrix
    QMatrix = np.linalg.inv(np.dot(GMatrix.T, GMatrix))
    QDiag = np.diag(QMatrix)

    # Compute the DOPS
    PosInfo["Hdop"] = np.sqrt(QDiag[0] + QDiag[1])
    PosInfo["Vdop"] = np.sqrt(QDiag[2])
    PosInfo["Pdop"] = np.sqrt(QDiag[0] + QDiag[1] + QDiag[2])
    PosInfo["Tdop"] = np.sqrt(QDiag[3])


def computeD(GMatrix, WMatrix):

    return np.linalg.inv(np.linalg.multi_dot([GMatrix.T, WMatrix, GMatrix]))


def computeS(GMatrix, WMatrix):

    return np.linalg.multi_dot([np.linalg.inv(np.linalg.multi_dot([GMatrix.T, WMatrix, GMatrix])), GMatrix.T, WMatrix])


def computePL(GMatrix, WMatrix, PosInfo, Mode):

    DMatrix = computeD(GMatrix, WMatrix)
    DDiag1 = np.diag(DMatrix)
    DDiag2 = np.diag(DMatrix, k = 1)

    PosInfo["Hpl"] = np.sqrt(((DDiag1[0] + DDiag1[1])/2) + np.sqrt(((DDiag1[0] - DDiag1[1])/2)**2 + DDiag2[0]**2)) * Const.MOPS_KH_PA
    PosInfo["Vpl"] = np.sqrt(DDiag1[2]) * Const.MOPS_KV_PA


def computeSpvtSolution(Conf, RcvrInfo, CorrInfo, Mode):
    
    # Initialize output
    PosInfo = OrderedDict({
            "Sod": 0,               # Second of day
            "Doy": 0,               # Day of year
            "Lon": 0.0,             # Receiver estimated longitude
            "Lat": 0.0,             # Receiver estimated latitude
            "Alt": 0.0,             # Receiver estimated altitude
            "Clk": 0.0,             # Receiver estimated clock
            "Sol": 0,               # 0: No solution 1: PA Sol 2: NPA Sol
            "NumSatVis": 0,         # Number of visible satellites
            "NumSatSol": 0,         # Number of visible satellites in solution
            "Hpe": 0.0,             # HPE 
            "Vpe": 0.0,             # VPE 
            "Epe": 0.0,             # EPE
            "Npe": 0.0,             # NPE 
            "Hpl": 0.0,             # HPL
            "Vpl": 0.0,             # VPL
            "Hsi": 0.0,             # Horiontal Safety Index
            "Vsi": 0.0,             # Vertical Safety Index
            "Hdop": 0.0,            # HDOP
            "Vdop": 0.0,            # VDOP
            "Pdop": 0.0,            # PDOP
            "Tdop": 0.0,            # TDOP
    }) # End of PosInfo

    PosInfo["Sod"] = CorrInfo[CorrIdx["SOD"]]
    PosInfo["Doy"] = CorrInfo[CorrIdx["DOY"]]
    PosInfo["Lon"] = float(RcvrInfo[RcvrIdx["LON"]])
    PosInfo["Lat"] = float(RcvrInfo[RcvrIdx["LAT"]])
    PosInfo["Alt"] = float(RcvrInfo[RcvrIdx["ALT"]])

    GMatrix = []
    WMatrix = []
    Weights = []

    for SatCorrInfo in CorrInfo.values():

        PosInfo["NumSatSol"] += 1  if SatCorrInfo["Flag"] == 1 else 0
        
        GMatrixRow = computeGRow(SatCorrInfo)

        GMatrix = np.vstack([GMatrix, GMatrixRow])

        Weights.append(1 / (SatCorrInfo["SigmaUere"]) ** 2)

    WMatrix = np.diag(Weights)

    if PosInfo["NumSatSol"] >= Const.MIN_NUM_SATS_PVT:

            computeDop(GMatrix, PosInfo)

            if PosInfo["Pdop"] < float(Conf["PDOP_MAX"]):
                # Compute the S matrix
                SMatrix = computeS(GMatrix, WMatrix)
                # Call WLSQ function
                wlsq(Conf, CorrInfo, PosInfo, SMatrix, Mode)
                # Compute protection levels
                computePL(GMatrix, WMatrix, PosInfo, Mode)
                # Compute safety indexes
                PosInfo["Hsi"] = PosInfo["Hpe"] / PosInfo["Hpl"]
                PosInfo["Vsi"] = PosInfo["Vpe"] / PosInfo["Vpl"]
                # Update intermediate performances
    
    return PosInfo



