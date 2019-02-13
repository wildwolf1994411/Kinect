from scipy.spatial.distance import _validate_vector
from scipy.ndimage.filters import gaussian_filter1d as gf
from scipy.ndimage.filters import gaussian_filter as gf_2D
from scipy.linalg import norm
from collections import defaultdict
from w_fastdtw import fastdtw
import numpy as np
from scipy.signal import argrelextrema
from scipy import signal
from dataoutput import Dataoutput
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
        self._done         = False
        #self.do_once       = False
        self.decTh         = 1800
        self.cnt           = 0
        self.distp_prev    = 0
        self.distp_cmp     = np.inf
        self.oidx          = 0  # initail
        self.gt_idx        = 0
        self.Ani_idx       = 0
        self.presv_size    = 0
        self.idxlist       = []
        self.idx_cmp       = 0
        self.fcnt          = 0
        self.srchfw        = 10  # forward search range
        self.srchbw        = 20  # backward search range
        self.error         = []
        # updatable parameters
        self.dpfirst       = {}
        self.dist_p        = {}
        self.deflag_mul    = defaultdict(lambda: (bool(False)))
        self.seqlist       = np.array([])
        self.seqlist_reg   = np.array([])
        self.seqlist_gf    = np.array([])
        self.dcnt          = 0
        self.chk_flag      = False
        self.deflag        = False  # decreasing flag
        self.onedeflag     = False
        self.segini        = True
        self.evalstr       = ''
        self.offset        = 0
        self.ngframe       = []

    def clip(self, seqlist, exeno):
        """ try find the subsequence from current sequence
        """
        tgrad = 0
        for ii in [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17]:
            tgrad += (np.gradient(gf(seqlist[:, ii], 1))**2)*self.jweight[ii]
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
        self.deflag_mul  = defaultdict(lambda: (bool(False)))
        self.cnt         = 0
        self.dpfirst     = {}
        self.dist_p      = {}
        self.deflag      = False
        self.onedeflag   = False
        self.segini      = True

    def matching(self, reconJ, gt_data, exeno, lowpass=True):
        """the main part of dtw matching algorithm
        """
        # self.fcnt += 1
        if self.segini:  # new segement/movement start
            self.segini = False
            # self.Ani_idx = self.aniorder[exeno][self.Ani_idx]
            if len(self.order[self.oidx]) == 1:
                self.gt_idx = self.order[self.oidx][0]
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
                if len(self.order[self.oidx]) > 1:
                    if self.seqlist.shape[0] > 1:
                        result = self.clip(self.seqlist, exeno)
                        if result != []:
                            endidx = result[0]
                            if self.seqlist[endidx, 7] < 150:
                                minidx = 2
                            else:
                                minidx = 3
                            self.gt_idx = minidx
                            self.idxlist.append(self.gt_idx)
                            self.evalstr = 'well done'
                            self.seg_update(endidx)
                else:
                    test_data_p = self.seqlist + np.atleast_2d((gt_data[self.gt_idx][0, :]-self.seqlist[0, :]))
                    self.dist_p, _ = fastdtw(gt_data[self.gt_idx], test_data_p, self.jweight, dist=self.wt_euclidean)
                    if (self.seqlist.shape[0] == 1+self.presv_size):  # new movement initail setting
                        self.dpfirst, _ = fastdtw(gt_data[self.gt_idx], test_data_p[:2], self.jweight, dist=self.wt_euclidean)
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
            test_data_p = self.seqlist + np.atleast_2d((gt_data[self.gt_idx][0, :] - self.seqlist[0, :]))
            self.dist_p, path_p = fastdtw(gt_data[self.gt_idx], test_data_p, self.jweight, dist=self.wt_euclidean)
            if self.chk_flag:  # in check global min status
                self.cnt += 1
                if self.dist_p < self.distp_cmp:  # find smaller value
                    self.cnt = 1
                    self.distp_cmp = self.dist_p
                    self.idx_cmp = self.seqlist.shape[0]
                    print(' ==== reset ====')
                elif self.cnt == self.srchfw:
                    self.evalstr = 'Well done'
                    self.chk_flag = False
                    tgrad = 0
                    for ii in xrange(self.seqlist.shape[1]):  # maybe can include jweight
                        tgrad += (np.gradient(gf(self.seqlist[:, ii], 1))**2)*self.jweight[ii]
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

    def run(self, reconJ, gt_data, exeno, surface=None, evalinst=None, ratio=1, stype=2, \
            lhs=0, rhs=0, dmap=[], bdry=[], frameno=0, lowpass=True):
    #def run(self, exer, ):
        """ according to different exercise, doing different processing
        """





        if not exer.order[self.oidx] == 'end':
            if exer.no == 1:
                if exer.cntdown <= 0:
                    if self.offset == 0:
                        self.offset = frameno
                    if len(exer.holdlist) == 0:  # hand in the holding state or not
                        exer.holdlist = reconJ
                    else:
                        exer.holdlist = np.vstack([exer.holdlist, reconJ]) 
                        if np.sum(np.abs(exer.holdlist[0]-exer.holdlist[-1])[exer.jweight[exer.no] != 0]) > 400:
                            exer.holdstate = False
                            
                    if exer.holdstate:
                        evalinst.blit_text(surface, exer.no, ratio, stype, 'Starting breath in/out', 1, 'red')

                        self.breathIO(bdry, dmap)
                    else:
                        if not self.do_once:
                            self.breath_analyze(self.offset)
                            self.do_once = True
                            self._done = True
                else:
                    # self.io.typetext(surface,'will Starting at '+str(np.round(self.cntdown/30., 2))+' second' ,(20, surface.get_height()*0.75),(255, 0, 0))
                    evalinst.blit_text(surface, exeno, ratio, stype, 'will Starting at '+str(np.round(self.cntdown/30., 2))+' second', 1)
                    self.cntdown -= 1
            elif exeno == 2:
                if self.order[exeno][self.oidx] == [2]:
                    if len(self.holdlist) == 0:  # hand in the holding state or not
                       self.holdlist = reconJ
                    else:
                        self.holdlist = np.vstack([self.holdlist, reconJ]) 
                        # print np.sum(np.abs(self.holdlist[0]-self.holdlist[-1])[self.jweight[2] != 0])
                        if np.sum(np.abs(self.holdlist[0]-self.holdlist[-1])[self.jweight[2] != 0]) > 1000:
                            self.holdstate = False
                    if self.holdstate:
                        # self.io.typetext(surface,'Starting breath in (hand close) and breath out (hand open)' ,(20, surface.get_height()*0.75), (255, 0, 0))
                        evalinst.blit_text(surface, exeno, ratio, stype, 'Starting breath in (hand close) and breath out (hand open)', 1)
                        self.handstate(lhs, rhs)
                        self.breathIO(bdry, dmap)
                    else:
                        if not self.do_once:
                            self.breath_analyze(self.offset)
                            self.hand_analyze(self.offset)
                            self.do_once = True                        
                        self.matching(reconJ, gt_data, exeno)
                else:
                    self.matching(reconJ, gt_data, exeno)    
            elif exeno == 3:
                self.matching(reconJ, gt_data, exeno)
                if self.idxlist.count(3) > 4:
                    evalinst.blit_text(surface, exeno, ratio, stype, 'Only need to do 4 times', 3)
                elif self.idxlist.count(3) > 0:
                   evalinst.blit_text(surface, exeno, ratio, stype, str(4-min(self.idxlist.count(3), self.idxlist.count(4))) + ' to go !!', 3, (55,173,245,255))
            elif exeno == 4:
                self.matching(reconJ, gt_data, exeno)
                if self.idxlist.count(3) > 4:
                    evalinst.blit_text(surface, exeno, ratio, stype, 'Only need to do 4 times', 3)
                elif self.idxlist.count(3) > 0:
                   evalinst.blit_text(surface, exeno, ratio, stype, str(4-min(self.idxlist.count(3), self.idxlist.count(4))) + ' to go !!', 3, (55,173,245,255))                
            else:
                raise ImportError('No such exercise !!')
        else:
            print('================= exe END ======================')
            self._done = True
  
        
                