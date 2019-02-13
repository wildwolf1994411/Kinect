import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter as gf_2D
from scipy.ndimage.filters import gaussian_filter1d as gf
from initial_param.kinect_para import Kinect_para
import inflect
import pdb

class Breath_status(object):
    """ detect breathing status
    """
    def __init__(self):
        self.ref_bdry      = np.array([])
        self.ref_dmap      = None
        self.breath_list   = []
        self.breath        = None
        self.ngframe       = []
        self.missingbreath = []
        self.ana_ary       = []
        self.breath_in     = []
        self.breath_out    = []
        self.max_ary       = np.array([[0, 0]])
        self.min_ary       = np.array([[0, 0]])
        self.max_len       = 1
        self.min_len       = 1
        self.plot_flag     = False
        self.brth_out_flag = False
        self.cnvt          = inflect.engine()  # converting numerals into ordinals
        self.kpm         = Kinect_para()        
        #save in log
        self.sync_rate = 0
        self.brth_diff = []
        # default parameters
        self.cnt     = 0
        self.do      = False
        self.err     = []
        self.errsum  = []
        self.evalstr = ''
        self.eval    = ''

    # def bodystraight(self, joints, th=20):
    #     """ check whether body is straight or not
    #     """
    #     print joints.shape[0]
    #     if joints.shape[0] == 21:  # only use limb joint
    #         offset = 12
    #     else:
    #         offset = 0
    #     torso_z = np.mean([joints[self.kpm.SpineBase_z-offset], joints[self.kpm.SpineMid_z-offset]])
    #     if torso_z-joints[self.kpm.Neck_z-offset] > th and torso_z-joints[self.kpm.Head_z-offset] > th:
    #         self.evalstr += 'Please stand straight.\n'
    #         return False
    #     return True

    def rm_pulse(self, ary, th=10):
        """ remove small pulse in the binary array
        """
        split_ary = np.split(ary, np.where(np.diff(ary)!=0)[0]+1)
        ary_len = [len(a) for a in split_ary]
        merge_idx = np.where(np.array(ary_len) < th)[0]
        if len(merge_idx) > 0:
            ary_idx = [sum(ary_len[:i]) for i in xrange(1, len(ary_len))]
            ary_idx.append(len(ary))
            for i in merge_idx:
                if i == 0:
                    ary[:ary_idx[i]] = ary[ary_idx[i]]
                else:
                    ary[ary_idx[i-1]:ary_idx[i]] = ary[ary_idx[i-1]-1]
        return ary

    def breathextract(self, bdry, dmap):
        """according to the depth map in the chest region,
           detect breathe in and breathe out.
        """
        cur_bdry = np.array([bdry[0][1], bdry[3][1], bdry[1][0], bdry[2][0]])
        if len(self.ref_bdry) == 0:
            # setup reference frame's boundary (up, down, left and right)
            self.ref_bdry = cur_bdry
            self.ref_dmap = dmap
        else:
            ubdry = np.array([int(min(cur_bdry[0], self.ref_bdry[0])),
                              int(max(cur_bdry[1], self.ref_bdry[1])),
                              int(max(cur_bdry[2], self.ref_bdry[2])),
                              int(min(cur_bdry[3], self.ref_bdry[3]))])
            blk_diff = gf_2D((dmap.astype(float)-self.ref_dmap.astype(float))[ubdry[1]:ubdry[0], ubdry[2]:ubdry[3]], 5)
            self.breath_list.append(np.mean(blk_diff))

            if len(self.breath_list) == 1:
                self.max_ary = np.array([[0, self.breath_list[0]]])
                self.min_ary = np.array([[0, self.breath_list[0]]])
                self.ana_ary = [[0, 1, self.breath_list[0]]]

    def breath_analyze(self, th=10):
        """ Analyze the human and breathe in/out behavior
        """
        for i in xrange(len(self.ana_ary)):
            if self.ana_ary[i][1] == 0:
                self.breath_in.append(self.ana_ary[i][0])
            else:
                self.breath_out.append(self.ana_ary[i][0])
        self.breath = np.sort(np.hstack([self.breath_in, self.breath_out])).astype(int)

        b_in = []
        b_out = []
        delidx = []

        if len(self.breath) != 0:
            for i, j in zip(self.breath[:-1], self.breath[1:]):
                try:
                    breath_diff = self.breath_list[j]-self.breath_list[i]
                except:
                    break
                self.brth_diff.append(abs(breath_diff))
                if abs(breath_diff) > 10:  # really breath in/out
                    if abs(breath_diff) < 30:  # not deep breath
                        if breath_diff > 0:  # breath out
                            print('breathe out from frame '+str(i)+' to frame '+str(j)+
                                  ' <== breathing is not deep enough')
                            b_out.append(j-i)
                            self.ngframe.append((i+j)/2)
                        else:  # breath in
                            print('breathe in from frame '+str(i)+' to frame '+str(j)+
                                  ' <== breathing is not deep enough')
                            b_in.append(j-i)
                            self.ngframe.append((i+j)/2)
                    else:
                        if breath_diff > 0:  # breath out
                            print('breathe out from frame '+str(i)+' to frame '+str(j))
                            b_out.append(j-i)
                        else:  # breath in
                            print('breathe in from frame '+str(i)+' to frame '+str(j))
                            b_in.append(j-i)
                else:
                    delidx.append(np.argwhere(self.breath == j)[0][0])
            if len(delidx) > 0:
                self.breath = np.delete(self.breath, np.array(delidx))
            print('\naverage breathe out freq is: '+str(np.round(30./np.mean(b_out), 2))+' Hz')
            print('\naverage breathe in freq is: '+str(np.round(30./np.mean(b_in), 2))+' Hz')
        else:
            # raise ImportError('Doing too fast !! please redo again !!')
            self.evalstr = 'Doing too fast !! please redo again !!\n'
    def brth_hand_sync(self, lhopen, lhclose):
        """calculate breathe and hand open/close relation
        """
        hand = np.sort(np.hstack([lhopen, lhclose]))
        if hand[0] == lhopen[0]:  # first term is open
            mode = 'open'
        else:
            mode = 'close'
        hand_trunc = np.vstack([hand, np.roll(hand, -1)])[:, :-1].T
        hand_trunc = np.vstack([hand_trunc, np.array([hand[-1], len(self.breath_list)-1])])
        hand_trunc[:,0] -= 5  # wide the range by 5 frames
        hand_trunc[:,1] += 5  # wide the range by 5 frames
        if mode == 'close':
            hand_trunc_close = hand_trunc[::2, :]
            hand_trunc_open = hand_trunc[1::2, :]
        else:
            hand_trunc_close = hand_trunc[1::2, :]
            hand_trunc_open = hand_trunc[::2, :]

        hand_chk = np.ones(len(hand_trunc))
        cnt = 0
        for idx, i in enumerate(self.breath_in):
            loc = np.where((i >= hand_trunc_close[:, 0]) & (i <= hand_trunc_close[:, 1]))[0]
            if len(loc) == 1:
                cnt += 1
                if (2*loc) < len(hand_trunc):
                    hand_chk[2*loc] = 0
            elif len(loc) == 0:
                pass
            else:
                print hand_trunc
        for idx, i in enumerate(self.breath_out):
            loc = np.where((i >= hand_trunc_open[:, 0]) & (i <= hand_trunc_open[:, 1]))[0]
            if len(loc) == 1:
                cnt += 1
                if (2*loc) < len(hand_trunc):
                    hand_chk[2*loc+1] = 0
            elif len(loc) == 0:
                pass
            else:
                print hand_trunc
        self.missingbreath = hand_trunc[hand_chk == 1]

        self.sync_rate = min(cnt*1./len(hand_trunc)*100, 100)
        print('hand and breathing synchronize rate is '+str(np.round(self.sync_rate, 2))+'%')

    def local_minmax(self, seq1, seq2, th, minmax_str, rng=15, scale=3):
        """ finding local min or max depending on the argument minmax
        """
        breath_list = gf(self.breath_list, scale)
        if minmax_str == 'min':
            minmax = np.less
        elif minmax_str == 'max':
            minmax = np.greater
        pts = argrelextrema(breath_list, minmax, order=rng)[0]
        if len(pts) != 0:
            if (pts[-1] - seq1[-1][0] >= rng and minmax(breath_list[pts[-1]], th) and
                pts[-1] > seq2[-1, 0]):
                seq1 = np.vstack((seq1, np.array([pts[-1], breath_list[pts[-1]]])))
        return np.atleast_2d(seq1)

    def updata_minmax(self, seq, minmax_str):
        if minmax_str == 'min':
            minmax = np.less
            flag = 0
        elif minmax_str == 'max':
            minmax = np.greater
            flag = 1
        if len(self.breath_list) != 0:
            if minmax(self.breath_list[-1], seq[-1, 1]):
                # print('updata '+minmax_str+'fame ' +str(len(self.breath_list)))
                seq[-1] = [len(self.breath_list), self.breath_list[-1]]
                self.ana_ary[-1] = [len(self.breath_list), flag, self.breath_list[-1]]
        return seq

    def detect_brth(self, rng=10, scale=3):

        if self.brth_out_flag:
            self.min_ary = self.updata_minmax(self.min_ary, 'min')
            self.max_ary = self.local_minmax(self.max_ary, self.min_ary, self.min_ary[-1, 1]+10, 'max', scale=scale)
            if self.max_ary.shape[0] > self.max_len:
                # print ('find one max  ' +str(self.max_ary[-1, 0]))
                self.brth_out_flag = False
                self.cnt += 1
                if self.eval == '':
                    self.evalstr = 'Repitition done: Well done.'
                else:
                    self.evalstr = 'Repitition done.\n'+ self.eval
                    self.eval = ''
                self.ana_ary.append([self.max_ary[-1, 0], 1, self.max_ary[-1, 1]])
        # detect brth in
        else:
            self.max_ary = self.updata_minmax(self.max_ary, 'max')
            self.min_ary = self.local_minmax(self.min_ary, self.max_ary, self.max_ary[-1, 1]-10, 'min', scale=scale)
            if self.min_ary.shape[0] > self.min_len:
                # print ('find one min ' +str(self.min_ary[-1, 0]))
                self.brth_out_flag = True
                self.ana_ary.append([self.min_ary[-1, 0], 0, self.min_ary[-1, 1]])
                if np.abs(self.max_ary[-1, 1] - self.min_ary[-1, 1]) < 30:
                    self.evalstr = 'Please breathe deeper.\n'
                    self.eval = 'Please breathe deeper.\n'
                    self.err.append('The '+self.cnvt.ordinal(self.cnt+1)+ ' time try, is not deep enough.')
                    self.errsum.append('Breathing is not deep enough.\n')
        self.max_len = self.max_ary.shape[0]
        self.min_len = self.min_ary.shape[0]

    def run(self, bdry, dmap, scale=3):
        self.do = True
        self.breathextract(bdry, dmap)
        self.detect_brth(scale=scale)
