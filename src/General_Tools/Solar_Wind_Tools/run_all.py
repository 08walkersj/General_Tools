from window import circular_variance, coupling, dipole, time_shift
from download import download_omni_1min
import os
from datetime import datetime as dt

def run_all(save_path, omni_path=False, start=20, end=10, start_year=1981, end_year=False):
    if not (save_path.endswith('.h5') or save_path.endswith('.hdf5')):
        save_path+='.h5'
    if not omni_path:
        omni_path= save_path
    if not (omni_path.endswith('.h5') or omni_path.endswith('.hdf5')):
        omni_path+='.h5'
    if not os.path.isfile(omni_path):
        if not end_year:
            end_year= dt.now().year
        download_omni_1min(start_year, end_year, monthFirstYear=1, monthLastYear=12, path=omni_path)
    print('Circular Variance')
    circular_variance(omni_path, save_path, window= start+end)
    print('Coupling')
    coupling(omni_path, save_path, window=start+end)
    print('Dipole')
    dipole(omni_path, save_path, window=start+end)
    print('Time Shift')
    time_shift(omni_path, save_path, start, end)
