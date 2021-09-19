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