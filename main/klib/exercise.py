import numpy as np
import h5py, pdb


data2 = h5py.File('data/GT_V_data_mod_EX2.h5', 'r')
data3 = h5py.File('data/GT_V_data_mod_EX3.h5', 'r')
data4 = h5py.File('data/GT_V_data_mod_EX4.h5', 'r')


class Exercise(object):
    def __init__(self):
        # default parameters
        self.no = 0
        self.angle = []
        self.cntdown = 60
        self.limbjoints = True  # only need limb joints


class Exer1(Exercise):
    """ muscle tightening deep breating
    """
    def __init__(self):
        # default parameters
        self.no = 1
        self.angle = []
        self.cntdown = 60
        self.limbjoints = True
        # order
        self.order = {}
        self.order[0] = [1]
        self.order[1] = [2]
        self.order[2] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5

class Exer2(Exercise):
    """ over the head pumping
    """
    def __init__(self):
        # default parameters
        self.no = 2
        self.angle = []
        self.cntdown = 60
        self.limbjoints = True
        # reference subsequences
        self.gt_data = {}
        self.gt_data[1] = data2['GT_1'][:]
        self.gt_data[2] = data2['GT_2'][:]
        # order
        self.order = {}
        self.order[0] = [1]
        self.order[1] = [2]
        self.order[2] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5

class Exer3(Exercise):
    """push-up pumping
    """
    def __init__(self):
        # default parameters
        self.no = 3
        self.angle = []
        self.cntdown = 60
        self.limbjoints = True
        # reference subsequences
        self.gt_data = {}
        self.gt_data[1] = data3['GT_1'][:]
        self.gt_data[2] = data3['GT_2'][:]
        self.gt_data[3] = data3['GT_3'][:]
        self.gt_data[4] = data3['GT_4'][:]       
        # order
        self.order = {}
        self.order[0] = [1]
        self.order[1] = [3]
        self.order[2] = 'end'
        self.order[3] = [4]
        self.order[4] = [2, 3]
        self.order[5] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 9., 9., 9., 9., 9., 9.,
                                 0., 0., 0., 9., 9., 9., 9., 9., 9.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5

class Exer4(object):
    """ horizontal pumping
    """
    def __init__(self):
        # default parameters
        self.no = 4
        self.angle = []
        self.cntdown = 60
        self.limbjoints = True
        # reference subsequences
        self.gt_data = {}
        self.gt_data[1] = data4['GT_1'][:]
        self.gt_data[2] = data4['GT_2'][:]
        self.gt_data[3] = data4['GT_3'][:]
        self.gt_data[4] = data4['GT_4'][:]         
        # order
        self.order = {}
        self.order[0] = [1]
        self.order[1] = [3]
        self.order[2] = 'end'
        self.order[3] = [4]
        self.order[4] = [2, 3]
        self.order[5] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5

class Exer5(Exercise):
    """ reach to the sky
    """
    def __init__(self):
        # default parameters
        self.no = 5
        self.angle = []
        self.cntdown = 60
        self.limbjoints = False  # need limb joints + torso joints
        # weight
        self.jweight = np.array([3., 3., 3., 3., 3., 3., 3., 3., 3.,
                                 3., 3., 3., 3., 3., 3., 3., 3., 3.,
                                 3., 3., 3.])
        self.jweight = self.jweight/sum(self.jweight)*1.5

class Exer6(Exercise):
    """ shoulder roll
    """
    def __init__(self):
        # default parameters
        self.no = 6
        self.angle = []
        self.cntdown = 60
        self.limbjoints = False # need limb joints + torso joints
        self.hraise = False  # hand raise
        # weight
        self.jweight = np.array([3., 3., 3., 3., 3., 3., 3., 3., 3.,
                                 3., 3., 3., 3., 3., 3., 3., 3., 3.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5


class Exer7(Exercise):
    """ clasp and spread
    """
    def __init__(self):
        # default parameters
        self.no = 7
        self.angle = []
        self.cntdown = 60
        self.limbjoints = False  # need limb joints + torso joints
        # weight
        self.jweight = np.array([3., 3., 3., 9., 9., 9., 3., 3., 3.,
                                 3., 3., 3., 9., 9., 9., 3., 3., 3.,
                                 0., 0., 0.])
        self.jweight = self.jweight/sum(self.jweight)*1.5
