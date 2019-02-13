from scipy.spatial.distance import _validate_vector
from scipy.ndimage.filters import gaussian_filter1d as gf
from scipy.ndimage.filters import gaussian_filter as gf_2D
from scipy.linalg import norm
from collections import defaultdict
from w_fastdtw import fastdtw
import numpy as np
from scipy.signal import argrelextrema
from dataoutput import Dataoutput
from math import acos
import inflect
import pdb

class Dynamic_time_warping(object):
    """ Dynamic time warping class.
        in this clas we can basically find several subsequences
        from the total sequence.
        Way to extend the exercise database: 1. in initial function,
        add the exercise order ie order[M][N]. Here M represents the
        new exercise and N is equal to 2+ #segments in your exercise.
        2. setting the weight for each joint's coordinates
    """
    def __init__(self):
        """ initailize the order and weight for each exercise
            initailize dtw parameters
        """    
        # dtw parameters initialization
        self.io            = Dataoutput()
        self.decTh         = 1800
        self.distp_prev    = 0
        self.distp_cmp     = np.inf      
        self.gt_idx        = 0   
        self.idxlist       = []
        self.idx_cmp       = 0
        self.srchfw        = 10  # forward search range
        self.srchbw        = 20  # backward search range
        self.seqlist_gf    = np.array([])
        self.cnvt          = inflect.engine() 
        # updatable parameters
        self.fcnt          = 0
        self.dpfirst       = {}
        self.dist_p        = {}
        #self.deflag_mul    = defaultdict(lambda: (bool(False)))
        self.seqlist       = np.array([])
        self.seqlist_reg   = np.array([])
        self.presv_size    = 0
        self.oidx          = 0  # initail       
        self.chk_flag      = False
        self.deflag        = False  # decreasing flag
        self.segini        = True
        self.Ltangle      = []  # Armpit angle in T-pose
        self.Lcangle      = []  # Armpit angle in arm close
        self.Rtangle      = []  # Armpit angle in T-pose
        self.Rcangle      = []  # Armpit angle in arm close 
        #save in log
        # self.jspos = []  # record the joints position when finish one subsequence 
        # default parameters
        self.cnt     = 0
        self.do      = False
        self.err     = []
        self.errsum  = []
        self.evalstr = ''
        self.eval    = ''       

    def wt_euclidean(self, u, v, w):
        """ normal euclidean dist with the weighting
        """
        u = _validate_vector(u)
        v = _validate_vector(v)
        dist = norm(w*(u-v))
        return dist

    def clip(self, seqlist, weight):
        """ try find the subsequence from current sequence
        """
        tgrad = 0
        for ii in [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17]:
            tgrad += (np.gradient(gf(seqlist[:, ii], 1))**2)*weight[ii]
        tgrad = tgrad**0.5
        lcalminm = argrelextrema(tgrad, np.less, order=5)[0]
        foo = np.where(((tgrad < 1)*1) == 0)[0]
        if (len(foo) == 0) | (len(lcalminm) == []):
            return []
        else:
            lb = max(foo[0], 50)
            minm = []
            for ii in lcalminm[lcalminm > lb]:
                if tgrad[ii] < 1:
                    minm.append(ii)
            return minm

    def seg_update(self, endidx):
        """ update the dictionary content then reset the parameters
        """
        self.seqlist_reg = self.seqlist_reg[endidx+1:, :]  # update the seqlist
        self.presv_size  = self.seqlist_reg.shape[0]
        self.oidx        = self.gt_idx
        self.fcnt         = 0
        self.dpfirst     = {}
        self.dist_p      = {}
        self.deflag      = False
        self.segini      = True
        self.chk_flag    = False

    def joint_angle(self, reconJ, idx=[4, 5, 6], y_vec=np.array([0, 1, 0]) ,offset=0):
        """ finding the angle between 3 joints.
            default joints are left shld, elbow, wrist.
        """
        if reconJ.shape[0] == 33:
            offset = 4
        if idx[0] == 8:  # right arm
            offset += 3
        #  sholder -> Elbow 
        vec1 = np.array([reconJ[(offset+1)*3]-reconJ[(offset*3)],
                        reconJ[(offset+1)*3+1]-reconJ[(offset*3)+1],
                        reconJ[(offset+1)*3+2]-reconJ[(offset*3)+2]])
        # Wrist -> Elbow 
        vec2 = np.array([reconJ[(offset+1)*3]-reconJ[(offset+2)*3],
                        reconJ[(offset+1)*3+1]-reconJ[(offset+2)*3+1],
                        reconJ[(offset+1)*3+2]-reconJ[(offset+2)*3+2]])

        costheta_ampit = vec1.dot(-1*y_vec)/sum(vec1**2)**.5/sum(y_vec**2)**.5
        costheta_elbow = vec2.dot(-1*y_vec)/sum(vec2**2)**.5/sum(y_vec**2)**.5
        costheta_sew = vec1.dot(vec2)/sum(vec1**2)**.5/sum(vec2**2)**.5
        return np.array([acos(costheta_ampit), acos(costheta_elbow), acos(costheta_sew)])*180/np.pi

    def matching(self, reconJ, exer, exeno, lowpass=True):
        """the main part of dtw matching algorithm
        """
        self.do = True
        if self.segini:  # new segement/movement start
            self.segini = False
            if len(exer.order[self.oidx]) == 1:
                self.gt_idx = exer.order[self.oidx][0]
                self.idxlist.append(self.gt_idx)
        if len(self.seqlist_reg) == 0:  # build sequence list
            self.seqlist_reg = reconJ
            # print self.seqlist_reg.shape
            self.seqlist_reg = self.seqlist_reg.reshape(-1, 21)
            self.seqlist = self.seqlist_reg
        else:
            self.seqlist_reg = np.vstack([self.seqlist_reg, reconJ])
            self.seqlist_gf = gf(self.seqlist_reg, 3, axis=0)
            if not lowpass:
                self.seqlist = self.seqlist_reg
            else:
                self.seqlist = self.seqlist_gf
        if not self.deflag:  # Not yet decreasing
            if np.mod(self.seqlist.shape[0]-self.presv_size-1, 10) == 0:
                # check every 10 frames
                if len(exer.order[self.oidx]) > 1:
                    if self.seqlist.shape[0] > 1:
                        result = self.clip(self.seqlist, exer.jweight)
                        if result != []:
                            endidx = result[0]
                            if self.seqlist[endidx, 7] < 150:
                                minidx = 2
                            else:
                                minidx = 3
                            self.gt_idx = minidx
                            if self.gt_idx == 3:  # arm close in exer4, arms push down in exer3
                                if exeno == 4:
                                    self.Lcangle.append(min(self.joint_angle(reconJ)[:2]))
                                    self.Rcangle.append(min(self.joint_angle(reconJ, idx=[8, 9, 10])[:2]))
                                    if self.Lcangle[-1] < 80 or self.Rcangle[-1] < 80:
                                        self.evalstr = 'Please keep your arms horizontally.\n'
                                        self.eval = 'Please keep your arms horizontally.\n'
                                        self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(4)+1)+ ' time try, arms is not horizontal.')
                                        self.errsum.append('Hands is not horizontal.')
                                elif exeno == 3:
                                    self.Lcangle.append(self.joint_angle(reconJ)[2])
                                    self.Rcangle.append(self.joint_angle(reconJ, idx=[8, 9, 10])[2])                                 
                                    if self.Lcangle[-1] > 50 or self.Rcangle[-1] > 50:
                                        self.evalstr = 'Please push your arms lower.\n'
                                        self.eval = 'Please push your arms lower.\n'
                                        self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(4)+1)+ ' time try, arms is not lower enough.')
                                        self.errsum.append('Hands is not lower enough.')

                            self.idxlist.append(self.gt_idx)
                            if self.eval == '':
                                self.evalstr = 'Subsequence done: Well done.'
                            else:
                                self.evalstr = 'Subsequence done.\n'+self.eval
                                self.eval = ''
                            # self.jspos.append(reconJ)
                            self.seg_update(endidx)
                else:
                    test_data_p = self.seqlist + np.atleast_2d((exer.gt_data[self.gt_idx][0, :]-self.seqlist[0, :]))
                    self.dist_p, _ = fastdtw(exer.gt_data[self.gt_idx], test_data_p, exer.jweight, dist=self.wt_euclidean)
                    if (self.seqlist.shape[0] == 1+self.presv_size):  # new movement initail setting
                        self.dpfirst, _ = fastdtw(exer.gt_data[self.gt_idx], test_data_p[:2], exer.jweight, dist=self.wt_euclidean)
                        print('dpfirst is : %f' % self.dpfirst)
                    else:
                        print('de diff is :%f' % (self.dpfirst - self.dist_p))
                        if (self.dpfirst - self.dist_p) > self.decTh:
                            print('=========')
                            print('deflag on')
                            print('=========')
                            self.deflag = True
                            self.distp_prev = self.dist_p
        else:  # already start decreasing
            test_data_p = self.seqlist + np.atleast_2d((exer.gt_data[self.gt_idx][0, :] - self.seqlist[0, :]))
            self.dist_p, path_p = fastdtw(exer.gt_data[self.gt_idx], test_data_p, exer.jweight, dist=self.wt_euclidean)
            if self.chk_flag:  # in check global min status
                self.fcnt += 1
                if self.dist_p < self.distp_cmp:  # find smaller value
                    self.fcnt = 1
                    self.distp_cmp = self.dist_p
                    self.idx_cmp = self.seqlist.shape[0]
                    print(' ==== reset ====')
                elif self.fcnt == self.srchfw:
                    if exeno == 4:  # exercise 4
                        if self.gt_idx == 3:  # arm close 
                            self.Lcangle.append(min(self.joint_angle(reconJ)[:2]))
                            self.Rcangle.append(min(self.joint_angle(reconJ, idx=[8, 9, 10])[:2]))
                            if self.Lcangle[-1] < 80 or self.Rcangle[-1] < 80:
                                self.evalstr = 'Please keep your arms horizontally.\n'
                                self.eval = 'Please keep your arms horizontally.\n'
                                self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(4)+1)+ ' time try, arms is not horizontal.')
                                self.errsum.append('Hands is not horizontal.')
                        elif self.gt_idx == 4:  # T-pose
                            self.Ltangle.append(min(self.joint_angle(reconJ)[:2]))
                            self.Rtangle.append(min(self.joint_angle(reconJ, idx=[8, 9, 10])[:2]))
                            if self.Ltangle[-1] < 80 or self.Rtangle[-1] < 80:
                                self.evalstr = 'Please keep your arms horizontally.\n'
                                self.eval = 'Please keep your arms horizontally.\n'
                                self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(3)+1)+ ' time try, arms is not horizontal.')
                                self.errsum.append('Hands is not horizontal.')
                    elif exeno == 3:  # exercise 3
                        if self.gt_idx == 3:  # arms push down
                            self.Lcangle.append(self.joint_angle(reconJ)[2])
                            self.Rcangle.append(self.joint_angle(reconJ, idx=[8, 9, 10])[2])
                            if self.Lcangle[-1] > 50 or self.Rcangle[-1] > 50:
                                self.evalstr = 'Please push your arms lower.\n'
                                self.eval = 'Please push your arms lower.\n'
                                self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(4)+1)+ ' time try, arms is not lower enough.')
                                self.errsum.append('Hands is not lower enough.')
                        elif self.gt_idx == 4:  # arms raise up
                            self.Ltangle.append(np.mean(self.joint_angle(reconJ)[::2]))
                            self.Rtangle.append(np.mean(self.joint_angle(reconJ, idx=[8, 9, 10])[::2]))
                            if self.Ltangle[-1] < 160 or self.Rtangle[-1] < 160:
                                self.evalstr = 'Please straighten your arms.\n'
                                self.eval = 'Please straighten your arms.\n'
                                self.err.append('The '+self.cnvt.ordinal(self.idxlist.count(3)+1)+ ' time try, arms is not straight.')
                                self.errsum.append('Hands is not straight.')

                    if self.eval == '':
                        self.evalstr = 'Subsequence done: Well done.'
                    else:
                        self.evalstr = 'Subsequence done.\n'+self.eval
                        self.eval = ''        
                    # self.jspos.append(reconJ)
                    tgrad = 0
                    for ii in xrange(self.seqlist.shape[1]):  # maybe can include jweight
                        tgrad += (np.gradient(gf(self.seqlist[:, ii], 1))**2)*exer.jweight[ii]
                    tgrad = tgrad**0.5
                    endidx = np.argmin(tgrad[self.idx_cmp-self.srchbw:self.idx_cmp+self.srchfw-1])\
                                + (self.idx_cmp-self.srchbw)
                    self.seg_update(endidx)
            else:
                if (self.dist_p - self.distp_prev) > 0:  # turning point
                    print (' ==============  large ====================')
                    self.distp_cmp = self.distp_prev
                    self.idx_cmp = self.seqlist.shape[0]
                    self.chk_flag = True
            self.distp_prev = self.dist_p
