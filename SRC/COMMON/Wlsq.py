#!/usr/bin/env python
import numpy as np
from COMMON import GnssConstants as Const
from COMMON.Coordinates import llh2xyz

def buildResidualsVector(CorrInfo, PosInfo):
    PsrResiduals = []

    # Convert from LLH Coordinates to Cartesian XYZ to estimate
    # new geometrical range and thus the new residuals.
    RcvrPos = np.array(llh2xyz(PosInfo["Lon"], PosInfo["Lat"], PosInfo["Alt"]))

    # Loop over all satellites in CorrInfo
    for SatCorrInfo in CorrInfo.values():
        if SatCorrInfo["Flag"] == 1:
            # Satellite position in WGS84 reference frame
            SatPos = np.array([SatCorrInfo["SatX"], SatCorrInfo["SatY"], SatCorrInfo["SatZ"]])
            # Compute geometrical range
            GeomRange = np.linalg.norm(np.subtract(SatPos, RcvrPos))
            # Compute pseudo-range residuals
            PsrResiduals.append(SatCorrInfo["CorrPsr"] - PosInfo["Clk"] - GeomRange)

    return PsrResiduals

def wlsq(Conf, CorrInfo, PosInfo, SMatrix):

    i = 0
    NormRcvrPosDelta = 9999.9

    while i <= Conf["MAX_LSQ_ITER"] and NormRcvrPosDelta > Const.LSQ_DELTA_EPS:

        PsrResiduals = buildResidualsVector(CorrInfo, PosInfo)

        RcvrPosDelta = np.dot(SMatrix, PsrResiduals).flatten()

        NormRcvrPosDelta = np.linalg.norm(RcvrPosDelta)

        # Update Rcvr estimated Position in Geodetic (LLH) and Clock Bias
        # Deltas are in meters, have to be converted to radians (or degrees).
        PosInfo["Lat"] = PosInfo["Lat"] + RcvrPosDelta[1] / (np.deg2rad(Const.EARTH_RADIUS))
        PosInfo["Lon"] = PosInfo["Lon"] + RcvrPosDelta[0] / (Const.EARTH_RADIUS * np.cos(np.deg2rad(PosInfo["Lat"])))
        PosInfo["Alt"] = PosInfo["Alt"] + RcvrPosDelta[2]
        PosInfo["Clk"] = PosInfo["Clk"] + RcvrPosDelta[3]

        # Estimate ENU Position Errors and HPE and VPE
        PosInfo["Epe"] = PosInfo["Epe"] + RcvrPosDelta[0]
        PosInfo["Npe"] = PosInfo["Npe"] + RcvrPosDelta[1]
        PosInfo["Hpe"] = np.sqrt(PosInfo["Epe"] ** 2 + PosInfo["Npe"] ** 2)
        PosInfo["Vpe"] = PosInfo["Vpe"] + RcvrPosDelta[2]

        i += 1

    # If the wlsq iterative filter converges
    if i <= Conf["MAX_LSQ_ITER"]:
        # PA solution achieved
            PosInfo["Sol"] = 1