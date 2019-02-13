import numpy as np
from math import acos
from scipy.signal import argrelextrema
from initial_param.kinect_para import Kinect_para
from scipy.ndimage.filters import gaussian_filter1d as gf
import inflect,pdb

class Swing(object):
    """ Dectect if body bend to left or right.
        Also if arm is straight or not.
    """
    def __init__(self):
        self.angle_mean = []
        self.angel_le   = []
        self.angel_re   = []
        self.angle_ini  = 90.0
        self.bend_max   = []
        self.bend_min   = []
        self.cnvt       = inflect.engine()  # converting numerals into ordinals
        self.max_ary = np.array([[0, 0]])
        self.min_ary = np.array([[0, np.inf]])
        self.max_len = 1
        self.min_len = 1
        self.bend_th = 20
        self.kpm     = Kinect_para()
        self.bend_left = True
        # default parameters
        self.cnt     = 0
        self.do      = False
        self.err     = []
        self.errsum  = []
        self.evalstr = ''
        self.eval    = ''

    def vec_angle(self, vec1, vec2=np.array([1, 0, 0])):
        """ find the angle btw vec1 and vec2
            if vec2 is not given, set vec2 as [1, 0, 0] which represent horizontal vector
        """
        costheta = vec1.dot(vec2)/sum(vec1**2)**0.5/sum(vec2**2)**0.5
        return acos(costheta)*180/np.pi

    def body_angle(self, joints):
        """ calculate body bending angle
        """
        vec_SLEL = joints[self.kpm.LElbow_x:self.kpm.LElbow_z+1] - joints[self.kpm.LShld_x:self.kpm.LShld_z+1]
        vec_SRER = joints[self.kpm.RElbow_x:self.kpm.RElbow_z+1] - joints[self.kpm.RShld_x:self.kpm.RShld_z+1]
        vec_SE   = (vec_SRER + vec_SLEL)/2  # combine vec_SLEL and vec_SRER
        self.angle_mean.append(self.vec_angle(vec_SE))  # angle btw vec_se and horizontal vector
        # store left and right arm angles
        self.angel_le.append(self.vec_angle(joints[self.kpm.LElbow_x:self.kpm.LElbow_z+1] - joints[self.kpm.LShld_x:self.kpm.LShld_z+1],\
                                            joints[self.kpm.LElbow_x:self.kpm.LElbow_z+1] - joints[self.kpm.LWrist_x:self.kpm.LWrist_z+1]))
        self.angel_re.append(self.vec_angle(joints[self.kpm.RElbow_x:self.kpm.RElbow_z+1] - joints[self.kpm.RShld_x:self.kpm.RShld_z+1],\
                                            joints[self.kpm.RElbow_x:self.kpm.RElbow_z+1] - joints[self.kpm.RWrist_x:self.kpm.RWrist_z+1]))

    def local_minmax(self, seq, th, minmax, rng=15):
        """ finding local min or max depending on the argument minmax
        """
        angle_bending = gf(self.angle_mean, 3)
        pts = argrelextrema(angle_bending, minmax, order=rng)[0]
        if len(pts) != 0:
            if pts[-1] - seq[-1][0] >= rng and minmax(angle_bending[pts[-1]], th):
                seq = np.vstack((seq, np.array([pts[-1], angle_bending[pts[-1]]])))
            elif 0 < pts[-1]-seq[-1][0] < rng and minmax(angle_bending[pts[-1]], seq[-1][1]):
                seq[-1] = np.array([pts[-1], angle_bending[pts[-1]]])
        return np.atleast_2d(seq)

    def updata_minmax(self,seq,minmax_str):
        if minmax_str == 'min':
            minmax = np.less
            flag = 0
        elif minmax_str == 'max':
            minmax = np.greater
            flag = 1
        if len(self.angle_mean) != 0:
            if minmax(self.angle_mean[-1], seq[-1,1]):
                # print('updata '+minmax_str+'fame ' +str(seq[-1,0] ))
                seq[-1] = [len(self.angle_mean), self.angle_mean[-1]]
        return seq


    def bending(self, joints, rng=15):
        """ check body bending
        """ 
        if self.bend_left:               
            self.min_ary = self.updata_minmax(self.min_ary,'min')
            self.max_ary = self.local_minmax(self.max_ary, self.angle_ini+self.bend_th, np.greater, rng)  
            if self.max_ary.shape[0] > self.max_len:
                self.bend_left = False
                if self.eval == '':
                    self.evalstr = 'Repitition done: Well done.'
                else:
                    self.evalstr = 'Repitition done.\n'+self.eval
                    self.eval = ''
                print '========  left  ========='
                self.cnt += 1
                # print ('bend to left  ' +str(self.max_ary[-1, 0])+'\n')
        else:
            self.max_ary = self.updata_minmax(self.max_ary,'max')
            self.min_ary = self.local_minmax(self.min_ary, self.angle_ini-self.bend_th, np.less, rng)
            if self.min_ary.shape[0] > self.min_len:
                self.bend_left = True
                if self.eval == '':
                    self.evalstr = 'Repitition done: Well done.'
                else:
                    self.evalstr = 'Repitition done.\n'+self.eval
                    self.eval = ''
                print ' ========  right  ========='
                self.cnt += 1
                # print 'bend to right ' +str(self.min_ary[-1, 0])+'\n'
        self.max_len = self.max_ary.shape[0]
        self.min_len = self.min_ary.shape[0]

    def straight_detection(self, angle_lsit, lr, rng=15, th=130):
        """ check if the arm (wrist-elbow-shoulder) is straight
        """
        if len(angle_lsit) < rng:
            res = np.mean(angle_lsit)
        else:
            res = np.mean(angle_lsit[-rng:])
        if res < th:
            if not 'Make your '+ lr +' arm straight.' in self.evalstr:
                self.evalstr += 'Make your '+ lr +' arm straight.\n'
                if lr not in self.eval:
                    self.eval += 'Make your '+ lr +' arm straight.\n'
            self.err.append(lr+' arm is not straight in '+self.cnvt.ordinal(int(self.cnt/2)+1)+' time bending.')
            self.errsum.append('Hand is not straight.')

    def init_angle(self):
        """ initialize torso angle
        """
        if len(self.angle_mean) <= 15:
            self.angle_ini = np.mean(self.angle_mean)



    def run(self, joints):
        self.init_angle()
        self.body_angle(joints)
        self.bending(joints)
        self.straight_detection(self.angel_le, 'left')
        self.straight_detection(self.angel_re, 'right')
