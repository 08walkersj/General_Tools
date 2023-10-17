#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:41:07 2021

@author: simon
"""
import numpy as np
def newell_coupling_function(Vx, By, Bz):
    theta= np.arctan2(By, Bz)
    return abs((10**-3)*(abs(Vx)**(4/3))*(np.sqrt(By**2 + Bz**2)**(2/3))*np.sin(theta/2)**(8/3))