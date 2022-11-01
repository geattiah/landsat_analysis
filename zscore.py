# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# @Author:              Gifty Attiah
# @Date:                2021-11-27
# @Email:               geattiah@gmail.com
# @Last Modified By:    Gifty Attiah
# @Last Modified Time:  Not Tracked
# 
# PROGRAM DESCRIPTION:
# Compute Temperature Outliers
# ----------------------------------------------------------------------------

import os
import sys
import rioxarray as rxr
import geopandas as gpd
import csv
import scipy.stats as stats
import numpy as np
import rasterio as rio
from matplotlib import pyplot
import matplotlib.pyplot as plt
from rasterio.plot import show
from scipy.stats.morestats import Std_dev
 
 
temp_file = r"C:\Users\ReSEC2021\Downloads\LT05_L1TP_044015_19940701_Achilles_Lake_24.44_-11.34_10.31_033.TIF"
  
with rio.open(temp_file) as tempfile:
   
    t_file = tempfile.read(1)
    out_meta = tempfile.meta
    out_transform = tempfile.transform
    np.seterr(divide='ignore', invalid='ignore')

    t_file = np.where(((t_file - np.nanmean(t_file))/np.nanstd(t_file) < -3.5) ,np.NaN,t_file)
    t_file = np.where(((t_file - np.nanmean(t_file))/np.nanstd(t_file) >  3.5) ,np.NaN,t_file)
    #a_file = np.where(((t_file - np.nanmean(t_file))/np.nanstd(t_file) < -3.5) & ((t_file - np.nanmean(t_file))/np.nanstd(t_file) > 3.5),np.NaN,t_file)


    out_meta.update({"driver": "GTiff",
                    "height": t_file.shape[1],
                    #"width": t_file.shape[2],
                    "transform": out_transform})

    with rio.open("tt3"+ ".TIF", "w", **out_meta) as dest:
        dest.write(t_file,1)

    # ras_mean = np.nanmean(t_file)
    # print(ras_mean)
    # ras_std = np.nanstd(t_file)
    # print(ras_std)
    
    # zscore = (t_file - ras_mean)/ras_std
    # print(zscore.ravel())
    # for i in zscore.ravel():
    #     print(i)