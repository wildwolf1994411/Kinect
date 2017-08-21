# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 20:58:04 2017

mainly for test dtw in paper

@author: admin
"""
import _pickle as cPickle
import numpy as np
from scipy.spatial.distance import euclidean
import scipy.signal as signal
from fastdtw import fastdtw
import matplotlib.pyplot as plt
###################### product test data #####################################
GT_ex_src   = 'Andy_2017-03-06 02.17.39 PM_ex4_FPS30_motion_unified.pkl'
Test_ex_src = 'Andy_2016-12-15 04.15.27 PM_ex4_FPS30_motion_unified.pkl'
#===================== combine two dataset ===================================#
GT_ex      = cPickle.load(open(GT_ex_src,'rb') ,encoding = 'latin1')[18:19,30:].T
Test_ex    = cPickle.load(open(Test_ex_src,'rb') ,encoding = 'latin1')[18:19,30:].T

Test_ex    = Test_ex[60:,:]
GT_ex      = GT_ex[30:,:]

#=================== clip data =============================================#
#GT_ex               = GT_ex[0:100,:]
Th                  = 1
id_clip             = [0]
y                   = [0]
for i in range (21,GT_ex.shape[0]):
    if np.abs(np.sum(GT_ex[i-21:i-1,:]-GT_ex[i-20:i,:])) < Th:
        if i-id_clip[len(id_clip)-1]<=100:
            continue
        id_clip.append(i)
        y.append(0)
id_clip.append(GT_ex.shape[0])
y.append(0)

#===========================================================================#
id_f                 = 0
distant_list         = []
id_list              = []
count_IO = False

for j in range (len(id_clip)-1): 
    Test_ex_P  = Test_ex + np.atleast_2d((GT_ex[id_clip[j]]-Test_ex[id_f]))
    print(str(id_f)+'   '+str(id_clip[j])+'    '+str(id_clip[j+1]))
    for i in range (id_f+2,Test_ex.shape[0]):
        distance, path     = fastdtw(GT_ex[id_clip[j]:id_clip[j+1],:], Test_ex[id_f:i,:],  dist=euclidean)
        distant_list.append(distance)
        if np.abs(np.sum(GT_ex[i-21:i-1,:]-GT_ex[i-20:i,:])) < Th:
            if i-id_clip[len(id_clip)-1]<=100:
                continue
    plt.plot(Test_ex[0:id_f,0])
    plt.plot(GT_ex[0:id_clip[j+1],0])
    plt.plot(id_clip,y,'.m')
    plt.show()    

        

