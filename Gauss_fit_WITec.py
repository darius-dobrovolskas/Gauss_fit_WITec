# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:44:08 2020

@author: dd
version: 1.1

Combines spectra from WITec X-Axis and Y-Axis txt files
and fits each spectra with two (or one) Gaussian functions.

Set initial values in gmodel.make_params(...).
Use gmodel.set_param_hint(...) for precise control of each Gaussian parameter.

Fitted parameters and statistics are saved to txt files.
"""
import pandas as pd
import matplotlib.pyplot as plt
from numpy import exp, loadtxt
from lmfit import Model
from datetime import datetime
from tqdm import tqdm

start_time = datetime.now()

def gauss(x, amp1, x01, w1, y0): 
    return (amp1*exp(-(x-x01)**2 / (2*(w1**2))) +y0)

def twogauss(x, amp1, x01, w1, amp2, x02, w2, y0):
    return (amp1*exp(-(x-x01)**2 / (2*(w1**2))) + amp2*exp(-(x-x02)**2 / (2*(w2**2))) +y0)

#load data
data_folder = 'C:\\DARBAI\\Binning test\\InGaN\\'
xlines = loadtxt(data_folder + 'scan06 (X-Axis).txt')
ylines = loadtxt(data_folder + 'scan06 (Y-Axis).txt') #, max_rows = 10240

ny = int(len(ylines)/1024)  #each image has (n*m)*1024 points, 
                            #where n and m are line and column numbers 
                            #of the image
                            
# print('number of y spectra', ny)

bvalues_full = pd.DataFrame()

x = xlines

for i in tqdm(range(ny)):
    y = ylines[(i)*1024:(i+1)*1024] 
        
    gmodel = Model(gauss)   #<-- enter function name (gauss or twogauss)
    
    # precise control of Gauss function parameters --------
    # gmodel.set_param_hint('amp1', value=40, min=0)
    # gmodel.set_param_hint('x01', value=500, min=440, max=520)
    # gmodel.set_param_hint('w1', value=100, min=0, max=300)
    
    # gmodel.set_param_hint('amp2', value=70, min=0)
    # gmodel.set_param_hint('x02', value=1750, min=1750, max=1850)
    # gmodel.set_param_hint('w2', value=100, min=0, max=300)
    
    # gmodel.set_param_hint('y0', value=0, max=0)
    # ------------------------------------------------------
    # inital values of Gauss function
    params = gmodel.make_params(amp1=40, x01=484, w1=20,
                                # amp2=40, x02=500, w2=20,
                                y0=0)
    fit = gmodel.fit(y, params, x=x)
    
    bvalues_df = pd.DataFrame.from_records([fit.best_values]).round(decimals=2)
    bvalues_full = bvalues_full.append(bvalues_df)
    
#save fit results to file
bvalues_full = bvalues_full.reset_index(drop=True)
bvalues_full.to_csv(data_folder + 'fitted_values.txt',  index=False) 
bvalues_full.describe().round(2).to_csv(data_folder + 'STATS_fitted_values.txt')

#show fit of the last spectra for visual evaluation
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (a.u.)')
plt.plot(x, y, 'b-', label='data')
plt.plot(x, fit.best_fit, 'r-', label='fit')
plt.legend(loc='best')
plt.show()

print(bvalues_full)

print('Elapsed time', datetime.now()-start_time)