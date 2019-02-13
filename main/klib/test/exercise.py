class Exer1(object):

    def __init__(self):
        self.no = 1
        self.cntdown       = 90     
        # order
        self.order[0] = [1]
        self.order[1] = [2]
        self.order[2] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])/sum(self.jweight)*1.5

class Exer2(object):

    def __init__(self):
        self.no = 2
        self.btype         = 'out'
        self.missingbreath = []
        self.hstate        = np.array([])
        self.rawhstate     = np.array([0,0])
        # self.ref_dmap      = None
        # self.ref_bdry      = np.array([])
        # self.breath_list   = []
        # self.breath        = None
        # order
        self.orderd[0] = [1]
        self.orderd[1] = [2]
        self.orderd[2] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])/sum(self.jweight)*1.5

class Exer3(object):

    def __init__(self):
        self.no = 3
        # order
        self.order[0] = [1]
        self.order[1] = [3]
        self.order[2] = 'end'
        self.order[3] = [4]
        self.order[4] = [2, 3]
        self.order[5] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 9., 9., 9., 9., 9., 9.,
                                 0., 0., 0., 9., 9., 9., 9., 9., 9.,
                                 0., 0., 0.])/sum(self.jweight)*1.5

class Exer4(object):

    def __init__(self):
        self.no = 4
        # order
        self.order[0] = [1]
        self.order[1] = [3]
        self.order[2] = 'end'
        self.order[3] = [4]
        self.order[4] = [2, 3]
        self.order[5] = 'end'
        # weight
        self.jweight = np.array([0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0., 3., 3., 3., 9., 9., 9.,
                                 0., 0., 0.])/sum(self.jweight)*1.5