import os
import argparse
import multiprocessing
import fnmatch
import rasterio as rio
import glob
import numpy as np
import matplotlib.pyplot as plt
import fiona
from rasterio.plot import plotting_extent,show
from rasterio.mask import mask


dirs = "/home/gift/Documents/research/Landsat_air_temp/LC08_L1TP_047016_20190625_20190705_01_T1"
img = "/home/gift/Documents/Landsat/new_landsat_output/img"
#for dirs in allSubDirs:
for files in os.listdir(dirs):
    fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
    file_out = os.path.join(dirs, files)
    with rio.open(file_out) as lake_temp:
        l = lake_temp.read(1)
    p = l - 17.7
    p = np.absolute(p)
    p = np.round(p)

    cmap="GnBu"
    plt.imshow(p, cmap=cmap,interpolation="hermite")
    #plt.clim(0,7)
    plt.colorbar().set_label('Temperature (°C)')
    plt.title(str(files)[41:-4])#((str(files)[17:25])+(str(files)[40:-4]))
    #fig_loc = "/home/gift/Documents/research/images/LST"
    #fig_file = os.path.join(fig_loc,(str(files)[17:25])+(str(files)[40:-4]))
    #plt.savefig(fig_file)   # save the figure to file
    kwargs = lake_temp.meta
    kwargs.update(
        dtype=rio.float32,
        count=1,
        compress='lzw')
    
    with rio.open(os.path.join(img,files[:-3]) + ".tif", 'w', **kwargs) as dst:
        dst.write_band(1, p.astype(rio.float32))

plt.show()

