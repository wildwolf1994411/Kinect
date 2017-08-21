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
GT_ex      = cPickle.load(open(GT_ex_src,'rb') ,encoding = 'latin1')[18:,30:].T
Test_ex    = cPickle.load(open(Test_ex_src,'rb') ,encoding = 'latin1')[18:,30:].T

#h          = np.atleast_2d(signal.firwin(10,0.2).T)
#Test_ex    = signal.convolve(Test_ex.T,h).T
#GT_ex      = signal.convolve(GT_ex.T,h).T

#Test_ex    = Test_ex[60:,:]
GT_ex      = GT_ex[:,:]
Test_ex    = Test_ex[:,:]

 

################### apply DTW to data ######################################
e                   = 20

sita                = 6
distance_global     = []
distance_global_P   = []
distant_list        = []
count_global        = 0
distance_count      = 0
count_IO            = False
break_IO            = False
distance_previous   = np.inf
id_f                = 0
#=================== clip data =============================================#
#GT_ex               = GT_ex[0:100,:]
Th                  = 10
id_clip             = [0]
y                   = [0]
for i in range (21,GT_ex.shape[0]):
    if np.abs(np.sum(GT_ex[i-21:i-1,0]-GT_ex[i-20:i,0])) < Th:
        if i-id_clip[len(id_clip)-1]<=100:
            continue
        id_clip.append(i)
        y.append(0)
id_clip.append(GT_ex.shape[0])
y.append(0)

#===========================================================================#
id_list=[]
for j in range (len(id_clip)-1): 
    Test_ex_P  = Test_ex + np.atleast_2d((GT_ex[id_clip[j]]-Test_ex[id_f]))
    print(Test_ex_P.shape)
    print(str(id_f)+'   '+str(id_clip[j])+'    '+str(id_clip[j+1]))
    for i in range (id_f+50,Test_ex.shape[0]):
        distance, path     = fastdtw(GT_ex[id_clip[j]:id_clip[j+1],:], Test_ex[id_f:i,:],  dist=euclidean)
        distance_P, path_P = fastdtw(GT_ex[id_clip[j]:id_clip[j+1],:], Test_ex_P[id_f:i,:], dist=euclidean)
        distant_list.append(distance)
        if distance_count > distance_previous and count_IO == True :
            
            distance_count=distance_previous
            count_global  = 0
            distance_global   = []
            distance_global_P = []
            print ('find another local min in frame: '+str(i))
            print ('list reset')
            count_IO = False
        if distance > distance_previous and count_IO == False:
#            print(str(distance_P)+'    '+str(distance))
            count_IO       = True
            distance_count = distance_previous
            print ('find local min in frame: '+str(i))
        if count_IO :
#            print(count_global)
            distance_global.append(distance)
            distance_global_P.append(distance_P)
            count_global = count_global+1
        if count_global == e and count_IO == True:
            error             = np.abs(np.array(distance_global)-np.array(distance_global_P))\
                                /np.array(distance_global)
            error_mean        = np.mean(error)
            print ('error mean is: '+str(1/error_mean))
            if 1/error_mean <=sita:
                print('global min found going to break ')
                print('segment id is :'+str(i-20))
                id_f=i-20
                break
            count_IO      = False
            distance_count    = 0
            count_global  = 0
            distance_global   = []
            distance_global_P = []
        distance_previous= distance
        if i==Test_ex.shape[0]-1:
            break_IO   = True
            id_f       = i-20
            print('find bound program going to stop')
            
    id_list.append(id_f)      
    count_IO      = False
    distance_count    = 0
    count_global  = 0
    distance_global   = []
    distance_global_P = []
    plt.plot(Test_ex[0:id_f,0]-500)
    plt.plot(GT_ex[0:id_clip[j+1],0])
    plt.plot(id_clip,y,'.m')
    plt.show()
    if break_IO:
        break
    
