# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:29:08 2019

@author: Simon
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import warnings
def statusCheck(data, time, indicator):
#removes data that is equal to the indicator and removes its associated time
    index= np.where(data==indicator)
    data =np.delete(data, index)
    time =np.delete(time, index)
    return time, data

def Median(data):
    data.sort()
    if len(data)%2==0:
        median= (data[int((len(data))/2)] + data[int((len(data))/2 -1)])/2
    else:
        median= data[int((len(data)-1)/2)]
    return median


def Xbar(data):
#calculates the mean of the set of data
    s=0
    l= 0
    for i in range(len(data)):
        if data[i]== 9.999:
            l= l+1
        else:
            s= s+ data[i]
    mean= float(s/(len(data)-l))
    return mean
def standardDeviation(mean, data):
#calculates the standard deviation of the set of data
    t=0
    l= 0
    for i in range(len(data)):
        if data[i]== 9.999:
            l= l+1
        else:
            t= t+ (data[i]- mean)**2
    t= t/(len(data)-l)
    return (t)**0.5
def anomaly_removal(data, number_of_SDs, set_size, SD_lim):
#creates a set of data equal to the set size 
#and goes through the set looking for anomalies and removes them
    for i in range(len(data)-set_size):
        dummyArray= data[i: i+set_size]
        mean= Xbar(dummyArray)
        SD= standardDeviation(mean, dummyArray)
#finds how much each data point deviates from the mean of the set
        deviations= []
        for j in range(len(dummyArray)):
            if dummyArray[j]== 9.999:
                deviations.append(0)
            else:
                deviations.append(abs(dummyArray[j] - mean))
#finds the largest deviation
        m= max(deviations)
        scale= 5
#if the standard deviation is larger than the preset value 
#and the largest deviation is greater than a preset number of standard deviaitons
#then there is a possibilty of a bad peice of data
        while m>(number_of_SDs)*SD and SD>SD_lim:
            skip= False
#looks for a value that doesn't fit the set
            for k in range(len(deviations)):
                if deviations[k]== 0:
                    continue
                else:
                    if abs(deviations[k])> float((scale)*SD):
#if triggered the possible anomaly has been found
                        print('anomaly checked')
#a second set of data is created with the possible anomaly 
#and data after it with the set size at the preset value
#the value is then checked if it is still anomalous within the new data set
                        dummyArray2= data[i+k:i+k+set_size]
                        mean2= Xbar(dummyArray2)
                        SD2= standardDeviation(mean2, dummyArray2)
                        deviations2=[]
                        for j in range(len(dummyArray2)):
#ignores data with an indicator showing the data is bad
                            if dummyArray2[j]== 9.999:
                                deviations2.append(0)
                            else:
                                deviations2.append(abs(dummyArray2[j] - mean))
#if the data point is found to still be anomlous 
#then it is given a bad data indicator otherwise it is skipped
                        m2= max(deviations2)
                        if deviations2[0]==m2 or deviations2[0]>(number_of_SDs)*SD2:
                            data[i+k]= 9.999
                            print('anomaly removed')
                        else:
                            skip= True
            if skip==True:
                break
#if a value has been removed the first set is checked again
            dummyArray= data[i:i+set_size]
            mean= Xbar(dummyArray)
            scale= scale-0.0001
            deviations= []
            for j in range(len(dummyArray)):
#ignores data with an indicator showing the data is bad
                if dummyArray[j]== 9.999:
                    deviations.append(0)
                else:
                    deviations.append(abs(dummyArray[j] - mean))
            m= max(deviations)
#once the set is no longer considered to contain bad data it moves onto the next set
#the progress of how far the code has got through the data shown after each set is checked
        print('Progress:')
        print(str((i/(len(data)))*100) +'%')
    return data
def anomaly_removal(data, set_size, frequency, SD_Lim, anomaly_sig=2):
    positions= np.array(range(len(data)))
    split= len(data)%set_size
    anoms_list=[]
    for i in range(set_size//frequency):
        windows= np.split(data[:-split], len(data)//set_size)
        wind_positions= np.split(positions[:-split], len(data)//set_size)
        stds=np.nanstd(windows, axis=1)
        bad_windows= np.array(windows)[stds>SD_Lim]
        if len(bad_windows)==0:
            continue
        bad_wind_positions= np.array(wind_positions)[stds>SD_Lim]
        means= np.nanmean(bad_windows, axis=1)
        pos_anoms=np.abs(bad_windows-means)==np.nanmax(np.abs(bad_windows-means), axis=1)
        anoms_list.append(positions==bad_wind_positions[pos_anoms])
    data[np.sum(np.array(anoms_list), axis=0)>=2]=np.nan
    return data
def anomaly_removal_cyclic(data, set_size, SD_Lim, frequency=1, anomaly_sig=2, return_index=False):
    """
    Parameters
    ----------
    data : numpy.ndarray
        Data to be checked.
    set_size : int
        The window size .
    SD_Lim : int/float
        Windows with stnadard deviation greater than this limit will be checked for anomalies.
    frequency : int, optional
        Spacing between windows. The default is 1 which makes the windows across the set one data point at a time.
    anomaly_sig : int, optional
        The number of windows an anomaly must be found within before it is confirmed to be an anomaly. The default is 2.
    return_index : bool optional
        If true will return a boolean index for the location of the anomalous data. The default is False.
    Returns
    -------
    data : numpy.ndarray
        A version of the data set now containing nans where the anomlies were.
    """
    positions= np.array(range(len(data))) #an array that will allow the location of values within the dataset to be recorded, this is in case of duplicate values
    anoms_list=[] #list that will contain the boolean arrays stating where anomalies were found in each iteration
    for i in range(set_size//frequency):
        i*=frequency #allows the data be moved through by the set frequency
        array_end=len(data[i:])%set_size *-1 #decide where the array should end so it can be broken up into arrays of the set size
        duplicated= set_size-len(data)%set_size #decides how many data points will repeated in order to make an extra window that goes from the end of the array to the beggining
        if len(data)%set_size==0: #if the length of the data set is a multiple of the set size then no data points need to be repeated
            duplicated=0
        extra_wind= np.append(data[array_end:], data[:i+duplicated]) #Extra window that enables the method to be cyclic and go from the end of the array to the beginning
        extra_pos= np.append(positions[array_end:], positions[:i+duplicated]) #Positions associated with this extra window, in terms of the orginal data set
        if array_end==0: # just notation that allows the data[:array_end] to go up to the end of the data set
            array_end=None
        windows= np.split(data[i:array_end], len(data[i:array_end])//set_size) #Splitting the data set into windows of set size adding i allows the windows to be shifted across
        wind_positions= np.split(positions[i:array_end], len(data[i:array_end])//set_size) #Repeating the split on positions so it can keep track of the positions of each data point
        if array_end is not None: #If not using all data already
            windows.append(extra_wind) #Add extra window that goes from the end of the array to the start enabling the added knowledge that the data is cyclic
            wind_positions.append(extra_pos) #Track the positions of the extra window
        print(windows)
        stds=np.nanstd(windows, axis=1) #Calculates the standard deviation of the windows, can switch to another spread of data if another is more desirable e.g. Mean absolute value or range
        bad_windows= np.array(windows)[stds>SD_Lim] #Find the windows where the standard deviation exceeds the limit
        if len(bad_windows)==0: #If there aren't any windows that have an excessive standard deviation then it proceeds to the next interation
            continue
        bad_wind_positions= np.array(wind_positions)[stds>SD_Lim] #Find the positions of the data in the bad windows in terms of the orginal data set
        means= np.vstack(np.nanmean(bad_windows, axis=1)) #Calculate the mean of the bad windows
        pos_anoms=np.abs(bad_windows-means)==np.vstack(np.nanmax(np.abs(bad_windows-means), axis=1)) #find the positions of the data that are furthest from the mean in their window, in terms of the orginal data set
        anoms=np.in1d(positions, bad_wind_positions[pos_anoms]).astype(int) #Create array that is the same size as positions and is 1 where an anomaly is found as 0 elsewhere
        _, ind=np.unique(bad_wind_positions[pos_anoms], return_counts=True) #because of the extra window sometimes there is an overlap and a data point is checked twice in one loop so if its an anomaly both times that must be taken into account
        ind= bad_wind_positions[pos_anoms][ind>1] #positions of the duplicates in terms of the orginal data set
        anoms[ind]+=1 #making duplicate positions count twice making them now 2
        anoms_list.append(anoms) #add array of numbers denoting the anomalies to a list
    if len(data[np.sum(np.array(anoms_list), axis=0)>=anomaly_sig])!=0: #Check if any anomalies have actually been found
        data[np.sum(np.array(anoms_list), axis=0)>=anomaly_sig]=np.nan #look for where a data point is found to be an anomaly at least as many times as anomaly_sig
        if return_index:
            return data, np.sum(np.array(anoms_list), axis=0)>=anomaly_sig #return the new data with nans for the anomalies and the boolean index that indicates the positions of the anomalies
        else:
            return data #return the new data with nans for the anomalies
    else:
        print('No anomalies found') #let the user know that there were no anomalies found
        if return_index:
            return data, np.sum(np.array(anoms_list), axis=0)>=anomaly_sig #return orginal data and the boolean index that should all be False
        else:
            return data #return orginal data
def anomaly_removal(data, set_size, SD_Lim, frequency=1, anomaly_sig=2):
    """
    Parameters
    ----------
    data : numpy.ndarray
        Data to be checked.
    set_size : int
        The window size .
    SD_Lim : int/float
        Windows with standard deviation greater than this limit will be checked for anomalies.
    frequency : int, optional
        Spacing between windows. The default is 1 which makes the windows across the set one data point at a time.
    anomaly_sig : int, optional
        The number of windows an anomaly must be found within before it is confirmed to be an anomaly. The default is 2.
    Returns
    -------
    data : numpy.ndarray
        A version of the data set now containing nans where the anomlies were.
    """
    positions= np.array(range(len(data))) #an array that will allow the location of values within the dataset to be recorded, this is in case of duplicate values
    anoms_list=[] #List that will contain the boolean arrays stating where anomalies were found in each iteration
    for i in range(set_size//frequency):
        i*=frequency
        array_end=len(data[i:])%set_size *-1
        if array_end==0:
            array_end=None
        windows= np.split(data[i:array_end], len(data[i:array_end])//set_size) #Splitting the data set into windows of set size adding i allows the windows to be shifted across
        wind_positions= np.split(positions[i:array_end], len(data[i:array_end])//set_size)
        stds=np.nanstd(windows, axis=1)
        bad_windows= np.array(windows)[np.array(stds>SD_Lim).flatten()]
        if len(bad_windows)==0:
            continue
        bad_wind_positions= np.array(wind_positions)[np.array(stds>SD_Lim).flatten()]
        means= np.vstack(np.nanmean(bad_windows, axis=1))
        pos_anoms=np.array(np.abs(bad_windows-means)==np.vstack(np.nanmax(np.abs(bad_windows-means), axis=1))).flatten()
        anoms_list.append(np.in1d(positions, np.array(bad_wind_positions).flatten()[pos_anoms]))
    data[np.sum(np.array(anoms_list), axis=0)>=anomaly_sig]=np.nan
    return data
def Huber_Mean(data, sd_lim=1.5, lim= 0.1, iter_lim= 20, rm_nan=True):
    """
    Calculates the Huber Weighted Mean

    Parameters
    ----------
    data : numpy.ndarray
        Values to calculate the Huber Weighted Mean.
    sd_lim : float/int, optional
        How many standard deviations from the mean before weighting begins. The default is 1.5.
    lim : float, optional
        As a multiple of the orignal mean how close must two consecutive iterations of the mean be before returning the Huber Weighted Mean. The default is 0.1.
    iter_lim : int, optional
        How many iterations before the code breaks and assumes no better difference in the means can be found. The default is 20.
    rm_nan : Bool, optional
        Should nans be removed? The default is True.

    Raises
    ------
    ValueError
        Raised when the mean is nan and subsequently a Huber Weighted Mean cannot be found.

    Returns
    -------
    mu: Huber Weighted Mean.

    """
    if rm_nan:
        data=data[np.isfinite(data)]
    mu= np.mean(data, axis=data.ndim-1)
    sigma= np.std(data)
    delta=9.999e3*np.max(data)
    i= 0
    lim*=mu
    while np.all(delta> lim):
        if data.ndim==2:
            e= abs(data-np.vstack(mu))
        else:
            e= abs(data-mu)
        w= sd_lim*sigma/e
        w[w>=1]=1
        # w= np.min(np.vstack([np.ones(e.shape), sd_lim*sigma/e]), axis=0)
        mu2=np.average(data, weights= w, axis=data.ndim-1)
        delta= abs(mu-mu2)
        mu= mu2
        if i>iter_lim:
            print('iteration limit reached')
            break
        i+=1
        if np.any(mu==np.nan):
            raise ValueError('Mean is nan')
    return mu

def Huber_anomaly_removal(data, anomaly_threshold, Iter_Lim=5, **Huber_Mean_kwargs):
    data= data.copy()
    mean= Huber_Mean(data, **Huber_Mean_kwargs)
    variance= np.abs(data-mean)
    anomalies= np.any(variance>anomaly_threshold)
    count= 0
    positions=[]
    while anomalies and count<=Iter_Lim:
        positions.extend(np.where(variance>anomaly_threshold)[0])
        data[np.where(variance>anomaly_threshold)[0]]=np.nan
        mean= Huber_Mean(data, **Huber_Mean_kwargs)
        variance= np.abs(data-mean)
        anomalies= np.any(variance>anomaly_threshold)
        count+=1
    if count>=Iter_Lim:
        print('Anomaly removal iteration limit reached')
    std= np.sqrt(np.nansum((data-mean)**2)/np.sum(np.isfinite(data)))
    if std>anomaly_threshold:
        warnings.warn(f'Anomaly threshold ({anomaly_threshold}) is less than the standard deviation ({std}) of the anomaly removed dataset')
    print(f'{count} anomalies made nans')
    return data, np.array(positions)
    
if __name__=='__main__':
	eqb=np.array([65, 66, 63, 65, 75, 68,np.nan, 67, 60, 66, 66])
	d=anomaly_removal(eqb.copy(), 3, 4, 1, 1)
