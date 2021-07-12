# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# @Author:              Gifty Attiah
# @Date:                2021-05-05
# @Email:               geattiah@gmail.com
# @Last Modified By:    Gifty Attiah
# @Last Modified Time:  Not Tracked
# 
# PROGRAM DESCRIPTION:
# Load tiff file, flatten based on csv and perform calculattion and plot, ice thickness on small lakes
# ----------------------------------------------------------------------------

import csv
from PIL import Image
import pandas as pd
import numpy 
import os
import matplotlib.pyplot as plt

csv_file = pd.read_csv(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\thick.csv")
print(csv_file)

folder = r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis"

frame = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_Frame_Lake.tif")
grace = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_Grace_Lake.tif")
handle = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_Handle_Lake.tif")
stewart = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_Stewart_Lake.tif")
longg = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_Long_Lake.tif")
h22 = Image.open(r"C:\Users\ReSEC2021\OneDrive - Wilfrid Laurier University\Arc_Analysis\LC08_L1TP_047016_20190305_20190309_01_T1\LC08_L1TP_047016_20190305_20190309_01_T1_H22_Lake.tif")

f_num = numpy.array(frame)
g_num = numpy.array(grace)
h_num = numpy.array(handle)
s_num = numpy.array(stewart)
l_num = numpy.array(longg)
hh_num = numpy.array(h22)

h2_num = hh_num
print(h2_num.shape)

p = []
uni_temp = csv_file["Temp"].unique()
#print(uni_temp)
for i in uni_temp:
    p.append(float(i))
#print(p)

for i in uni_temp:
    d = csv_file.loc[csv_file["Temp"] == i,'grid_code'].min() 

b = [csv_file.loc[csv_file["Temp"] == i,'grid_code'].min() for i in uni_temp]
#print(b)
df = pd.DataFrame(uni_temp)

np_tick = dict(zip(uni_temp,b))

m = h2_num.flatten()
n = m.tolist()

q = [round(i,2) for i in n]
#print(q)  

def closest(lst, K):
      
     lst = numpy.asarray(lst)
     idx = (numpy.abs(lst - K)).argmin()
     return lst[idx]

su = []
for i in q:
    a = closest(p, i)
    su.append(a)
    #print(a)
#print(su)

kv = [(k, np_tick[k]) for k in su if k in np_tick]
#print(kv)

g = []
for key, value in kv:
    g.append(value)
#print(g)

new_g = [round(i,3) if i != 1.09329961 else 0 for i in g]
#print(new_g)

t = numpy.asarray(new_g)
#print(t)

t = numpy.reshape(t, (9, 12))
t[t == 0] = 'nan'
#print(t)

im = Image.fromarray(t)
im.save(os.path.join(folder,"h2.tiff"), "TIFF")

plt.imshow(t, cmap='hot')
plt.show()