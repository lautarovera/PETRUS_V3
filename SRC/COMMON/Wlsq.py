#!/usr/bin/env python

from COMMON import GnssConstants as Const

def wlsq(Conf, CorrInfo, PosInfo, SMatrix, Mode):

    i = 0

    while i <= Conf["MAX_LSQ_ITER"][0] and norm(RcvrPosDelta) > Const.LSQ_DELTA_EPS:
        
