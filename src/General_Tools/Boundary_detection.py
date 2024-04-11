#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 13:49:31 2021

@author: simon
"""
import numpy as np
from astropy.convolution import convolve, Box1DKernel
def turning_points(x, y):
    try:
        z=np.polyfit(x, y, 10)
        p=np.poly1d(z)
        dy=np.diff(p(np.linspace(x[0], x[-1])))
        return np.sum(np.diff(np.sign(dy))!=0)
    except:
        return 0
def boundary_detection(x, y, val_per=0.6, diff_per=0.5, standard_window=3, poly_window=5, pos2zero=True):
    if standard_window:
        smoothed= convolve(y, Box1DKernel(standard_window))
    else:
        smoothed= y 
    m= np.nanmin(smoothed)
    smoothed-=np.nanmin(smoothed)
    if np.nanmax(smoothed)*val_per +m>0 and pos2zero:
        val_per=0
    val_thresh= smoothed>np.nanmax(smoothed)*val_per
    if poly_window and turning_points(x[val_thresh], y[val_thresh])>2:
        smoothed= convolve(y, Box1DKernel(poly_window))
        m= np.nanmin(smoothed)
        smoothed-=np.nanmin(smoothed)
        val_thresh= smoothed>np.nanmax(smoothed)*val_per
        
    peak_ind= np.where(smoothed==np.nanmax(smoothed))[0][0]
    above_peak= np.array([False]*x.shape[0])
    above_peak[peak_ind+1:]=True
    below_peak= np.array([False]*x.shape[0])
    below_peak[:peak_ind]=True
    diff= np.zeros(x.shape)
    diff[::2][1:]= abs(np.diff(smoothed[1::2])/np.diff(x[1::2]))
    diff[1::2][:-1]= abs(np.diff(smoothed[::2])/np.diff(x[::2]))
    diff[(diff==0)|(~val_thresh)]=np.nan
    diff_thresh= (diff>np.nanmean(diff)*diff_per) & (np.isfinite(diff))
    try:
        i=np.min(np.where((diff_thresh)&(above_peak)))
        j=np.max(np.where((diff_thresh)&(below_peak)))
        above_peak[:i+1]=False
        below_peak[j:]=False
        return np.min(x[(~diff_thresh)&(above_peak)]), np.max(x[(~diff_thresh)&(below_peak)]), np.nanmax(smoothed)*val_per +m
    except ValueError:
        return np.nan, np.nan, np.nanmax(smoothed)*val_per + m
