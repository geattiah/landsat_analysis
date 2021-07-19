# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# @Author:              Gifty Attiah
# @Date:                2021-07-04
# @Email:               geattiah@gmail.com
# @Last Modified By:    Gifty Attiah
# @Last Modified Time:  Not Tracked
# 
# PROGRAM DESCRIPTION:
# Masking Landsat
# ----------------------------------------------------------------------------

import os
import sys
import shutil
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches, colors
#import seaborn as sns
import numpy as np
from numpy import ma
import xarray as xr
import rioxarray as rxr
import rasterio as rio
import earthpy as et
import earthpy.plot as ep
import earthpy.mask as em
from pymasker import LandsatMasker
from pymasker import LandsatConfidence

cloudcon_l_8_high = [2800,2804,2808,2812,6896,6900,6904,6908]
cloudcon_l_8_low = [2720,2722,2724,2728,2732,2976,2980,2984,2988,3744,3748,3752,3756,6816,6820,6824,6828,7072,7076,7080,7084,7840,7844,7848,7852]
cloudcon_l_8_med = [3744,2752,2756,2760,2764,3008,3012,3016,3020,3776,3780,3784,3788,6848,6852,6856,6860,7104,7108,7112,7116,7872,7876,7880,7884]
cloudsha_l_8 = [2976,2980,2984,2988,3008,3012,3016,2020,7072,7076,7080,7084,7104,7108,7112,7116]



landsat_folder = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Documents\Spatial_Data\landsat_test\LC08_L1TP_046016_20200620_20200707_01_T1.tar\LC08_L1TP_046016_20200620_20200707_01_T1"

quality = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Documents\Spatial_Data\landsat_test\LC08_L1TP_046016_20200620_20200707_01_T1.tar\LC08_L1TP_046016_20200620_20200707_01_T1\LC08_L1TP_046016_20200620_20200707_01_T1_BQA.TIF"

b2 = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Documents\Spatial_Data\landsat_test\LC08_L1TP_046016_20200620_20200707_01_T1.tar\LC08_L1TP_046016_20200620_20200707_01_T1\LC08_L1TP_046016_20200620_20200707_01_T1_B2.TIF"
#quality = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Documents\Spatial_Data\landsat_test\clip.tif"

cloud_l_8 = [2800,2804,2808,3744,2812,6896,6900,6904,6908,2976,2980,2984,2988,3008,3012,3016,2020,7072,7076,7080,7084,7104,7108,7112,7116]
cloud_l_8 = cloudcon_l_8_med + cloudcon_l_8_high + cloudsha_l_8
#cloud_l_8 = cloudsha_l_
bqa_quality = rxr.open_rasterio(quality).squeeze()

b2_open= rxr.open_rasterio(b2).squeeze()

print(bqa_quality.shape)


cl_mask = bqa_quality.isin(cloud_l_8)
#cl_mask = cl_mask.where(cl_mask)
np.unique(cl_mask)

masked = b2_open.where(~cl_mask)
masked = masked.where(masked != 0)

# ep.plot_bands(masked,
#               cmap="Greys",
#               title="Masked",
#               cbar=False)
# plt.show()
#cl_mask.to_raster(os.path.join(landsat_folder,"rio_mask.tif"))

masked.rio.to_raster(os.path.join(landsat_folder,"maskeded.tif"))
#cl_mask.rio.to_raster(os.path.join(landsat_folder,"c_mask.tif"))
#bqa_quality.plot.hist(color="purple")

# with rasterio.open(os.path.join(landsat_folder,'resultsm.tiff'), 
#                             'w',
#                             driver='GTiff',
#                             height=cl_mask.shape[0],
#                             width=cl_mask.shape[1],
#                             count=1,
#                             dtype=cl_mask.dtype,
#                             crs=src.crs,
#                             nodata=None, # change if data has nodata value
#                             transform=src.transform) as dst:
#                 dst.write(cl_mask.astype(rasterio.uint8), 1)



with rio.open(quality) as src:
    data = src.read()
    profile = src.profile

with rio.open(os.path.join(landsat_folder,'resultsm.tiff'), 'w', nbits=1, **profile) as dst:
    dst.write(cl_mask.astype(np.uint16),1)
#bqa_quality.squeeze().plot.imshow()
#plt.show()
# fig, ax = plt.subplots(figsize=(12, 8))

# im = ax.imshow(cl_mask,
#                cmap=plt.cm.get_cmap('tab20b', 2))

# cbar = ep.colorbar(im)
# cbar.set_ticks((0.25, .75))
# cbar.ax.set_yticklabels(["Clear Pixels", "Cloud / Shadow Pixels"])

# ax.set_title("Landsat Cloud Mask | Light Purple Pixels will be Masked")
# ax.set_axis_off()

# plt.show()

