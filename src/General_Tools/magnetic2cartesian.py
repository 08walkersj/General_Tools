import numpy as np
RE= 6.371E6
def mlt2azimuth(mlat, Dmlt):
    return ((Dmlt/12)*np.pi)*RE*np.cos(np.deg2rad(mlat))
