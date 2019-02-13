import numpy as np
from scipy import signal

class Hand_status(object):

    def __init__(self):
        self.hstate    = np.array([])
        self.rawhstate = np.array([0,0]) 
        # default parameters
        self.cnt     = 0
        self.do      = False
        self.err     = []
        self.errsum  = []
        self.evalstr = ''
        self.eval    = ''

    def hstus(self, hstus):
        if (hstus == 2): #Lhand open
            return 'Open'
        elif hstus == 0:
            return 'Unknown'
        elif hstus == 3:
            return 'Closed'
        elif hstus == 4:
            return 'Lasso'
        else:
            return 'Not detect'  

    def htext(self, lhstus, rhstus): 
        lstatus = self.hstus(lhstus)
        rstatus = self.hstus(rhstus)
        return 'Lhand : '+lstatus +'\nRhand : '+rstatus

    def find_pair_within(self, l1, l2, dist=10):
        """ from list 1 and list 2 find pairs
        """
        b = 0
        e = 0
        res = []
        for idx, a in enumerate(l1):
            while b < len(l2) and a - l2[b] > dist:
                b += 1
            while e < len(l2) and l2[e] - a <= dist:
                e += 1
            res.extend([(idx,b) for x in l2[b:e]])
        return res

    def hstus_proc(self, lhs, rhs):
        """ check the hand status and preprocess it.
            the value of the lhs and rhs represent the tracking
            state given foem Kinect sensor. 
            0: unknown
            1: not tracked
            2: open
            3: closed
            4: lasso
        """
        self.rawhstate = np.vstack([self.rawhstate, np.array([lhs,rhs]).reshape(-1, 2)])
        if lhs == 4:
            lhs = 0
        if rhs == 4:
            rhs = 0
        if (lhs == 0 | lhs == 1 ) and (rhs == 2 or rhs == 3): # if left hand is no tracking , using right
            lhs = rhs
        elif (rhs == 0 | rhs == 1 ) and (lhs == 2 or lhs == 3): # if right hand is no tracking , using left
            rhs = lhs
        # if hand state unknown, assign defalut state
        if lhs == 0:
            if len(self.hstate) == 0:
                lhs = 2
            else:
                lhs = self.hstate[-1, 0]
        if rhs == 0:
            if len(self.hstate) == 0:
                rhs = 2
            else:
                rhs = self.hstate[-1, 1]

        if len(self.hstate) == 0:
            self.hstate = np.array([lhs,rhs]).reshape(-1, 2)
            self.hstate = np.vstack([self.hstate, self.hstate])  # duplicate the data 
        else:
            self.hstate = np.vstack([self.hstate, np.array([lhs,rhs]).reshape(-1, 2)])

    def hstus_ana(self, offset=0, th=10):
        """Analyze the human and hand open/close behavior
        """
        self.do = True 
        # === hand close/open part ===
        foo = signal.medfilt(self.hstate, kernel_size=3)
        sync_rate = sum((foo[:, 0] == foo[:, 1])*1.)/len(foo[:, 0])*100
        print('left and right hand synchronize rate is '+str(np.round(sync_rate, 2))+'%')
        self.hstate[1:-1] = foo[1:-1]
        if np.sum(self.hstate[0]) != 4:
            self.err.append('two hands must open when you rise you arms')
        if np.sum(self.hstate[-1]) != 4:
            self.err.append('two hands must open when you put down your arms')
        hand_pulse = (self.hstate - np.roll(self.hstate, -1, axis=0))[:-1]
        lh         = np.where(hand_pulse[:, 0] != 0)[0]
        lh_open    = np.where(hand_pulse[:, 0] == 1)[0]
        lh_close   = np.where(hand_pulse[:, 0] == -1)[0]
        rh         = np.where(hand_pulse[:, 1] != 0)[0]
        rh_open    = np.where(hand_pulse[:, 1] == 1)[0]
        rh_close   = np.where(hand_pulse[:, 1] == -1)[0]
        # open test
        pair = self.find_pair_within(lh_open, rh_open)
        if len(lh_open) != len(rh_open):
            foo = np.array(pair)
            res = list(set(foo[:,0])-set(foo[:,1]))
            if len(lh_open) > len(rh_open):
                string = 'right hand'
            else:
                string = 'left hand'
            for i in res:
                self.err.append(string+' did not open at '+str(i+1)+' time')
                self.errsum.append('Hand did not open appropriately')
            print('hand open '+str(max(len(lh_open), len(rh_open)))+' times,')
        else:
            print('hand open '+str(len(lh_open))+' times')
        # close test
        pair = self.find_pair_within(lh_open, rh_open)
        if len(lh_close) != len(rh_close):
            foo = np.array(pair)
            res = list(set(foo[:,0])-set(foo[:,1]))
            if len(lh_close) > len(rh_close):
                string = 'right hand'
            else:
                string = 'left hand'
            for i in res:
                self.err.append(string+' did not close at '+str(i+1)+' time')
                self.errsum.append('Hand did not close appropriately')
            print('hand close '+str(max(len(lh_close), len(rh_close)))+' times,')
        else:
            print('hand close '+str(len(lh_close))+ ' times\n')
        return lh_open, lh_close
        