from exercise import Exer1
from dtw2 import Dynamic_time_warping as dtw
from breathstus import Breath_status

class Analysis(object):
    """ Analyze the exercise sequence 
    """
    def __init__(self):
        self.exer = {}
        self.exer[1] = Exer1()
        #
        self.dtw = dtw()
        self.brth = Breath_status()
        #
        self.do_once = False
        self._done = False
        self.offset = 0
        self.holdstate = True
        self.holdlist = np.array([])

    def run(self, exeno, reconJ, surface=None, evalinst=None, ratio=1, stype=2, dmap=[], bdry=[], frameno=0):
        if exeno == 1:
            if self.exer[1].cntdown <= 0:
                if self.offset == 0:
                    self.offset = frameno
                if len(self.holdlist) == 0:  # hand in the holding state or not
                    self.holdlist = reconJ
                else:
                    self.holdlist = np.vstack([self.holdlist, reconJ]) 
                    if np.sum(np.abs(self.holdlist[0]-self.holdlist[-1])\
                       [self.exer[1].jweight[exeno] != 0]) > 400:
                        self.holdstate = False
                if self.holdstate: 
                    evalinst.blit_text(surface, exeno, ratio, stype, 'Starting breath in/out', 1, 'red')
                    self.brth.breathIO(bdry, dmap)
                else:
                    if not self.do_once:
                        self.brth.breath_analyze(self.offset)
                        self.do_once = True
                        self._done = True            
            else:
                evalinst.blit_text(surface, self.exer[1].no, ratio, stype, 'will Starting at '\
                                   +str(np.round(self.exer[1].cntdown/30., 2))+' second', 1)
                self.exer[1].cntdown -= 1             

        elif exeno == 2:
            pass
        elif exeno == 3:
            pass
        elif exeno == 4:
            pass
        elif exeno == 5:
            pass
        elif exeno == 6:
            pass