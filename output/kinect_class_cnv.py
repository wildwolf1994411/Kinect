from kinect_normal_class import Kinect_3D_pts
from kinect_normal_class import Kinect_2D_pts
from collections import defaultdict
import os, glob
import cPickle
import numpy as np

src_path = "./output/"
dst_path = "./output/"

# dic_keys = ['joints', 'jointspts', 'depth_jointspts', ]

for infile in glob.glob(os.path.join(src_path, '*pkl')):
    data = cPickle.load(file(infile, 'rb'))
    newdata = []
    for i in xrange(len(data)):
        dataperframe = defaultdict(list)
        for j in data[0].keys():
            if j == 'joints':  # 3D
                dataperframe[j] = [None]*25
                for k in xrange(25):
                    dataperframe[j][k] = Kinect_3D_pts()
                    dataperframe[j][k].Position.x = data[i][j][k].Position.x
                    dataperframe[j][k].Position.y = data[i][j][k].Position.y
                    dataperframe[j][k].Position.z = data[i][j][k].Position.z
                    dataperframe[j][k].JointType = data[i][j][k].JointType
                    dataperframe[j][k].TrackingState = data[i][j][k].TrackingState

            elif j == 'depth_jointspts' or j == 'jointspts':  # 2D
                dataperframe[j] = [None]*25
                for k in xrange(25):
                    dataperframe[j][k] = Kinect_2D_pts()
                    dataperframe[j][k].x = data[i][j][k].x
                    dataperframe[j][k].y = data[i][j][k].y
            else:
                dataperframe[j] = data[i][j]
        newdata.append(dataperframe)
    name = dst_path + infile.split('\\')[-1].split('.')[0] + '_cnv.pkl'
    cPickle.dump(newdata, file(name, 'wb'))




