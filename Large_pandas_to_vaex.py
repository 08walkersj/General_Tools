#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 13:46:07 2022

@author: simon
"""
from progressbar import progressbar
import pandas as pd
import vaex as vx
import os
import numpy as np
import gc
def convert(in_put, out_put='./', copy_index=False, index_rename='index', key='main', chunksize=5_000_000):
    store= pd.HDFStore(in_put, mode='r')
    nrows=0
    max_value= np.ceil(store.get_storer(key).shape/chunksize)
    for i, df in progressbar(enumerate(store.select(key=key, chunksize=chunksize)), max_value=max_value):
        nrows+=len(df)
        dfvx= vx.from_pandas(df, copy_index=False)
        if copy_index:
            dfvx.rename('index', index_rename)
        dfvx.export_hdf5(out_put+f'batch{i:03d}_vaex.hdf5')
        gc.collect()
    store.close()
    data= vx.open(out_put+'batch*_vaex.hdf5')
    data.export_hdf5(out_put+'Combined_Data.hdf5')
    files= os.listdir(out_put)
    for file in files:
        if file.startswith('batch') and file.endswith('_vaex.hdf5'):
            os.remove(out_put+file)