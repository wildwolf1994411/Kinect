class Breath_status(object):

    def __init__(self):
        self.ref_bdry      = np.array([])
        self.ref_dmap      = None
        self.breath_list   = []
        self.breath        = None

    def breathIO(self, bdry, dmap):
        """according to the depth map in the chest region,
           detect breath in and breath out.
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
            blk_diff = gf_2D((dmap-self.ref_dmap)[ubdry[1]:ubdry[0], ubdry[2]:ubdry[3]], 5)
            self.breath_list.append(np.mean(blk_diff))

    def breath_analyze(self, offset=0, th=10):
        """ Analyze the human and breath in/out behavior
            
        """
        # breath part
        breath_gd = np.gradient(gf(self.breath_list, 10))
        breath_gd[breath_gd > 0] = 1
        breath_gd[breath_gd < 0] = 0
        breath_pulse = breath_gd[:-1]-np.roll(breath_gd, -1)[:-1]
        breath_in = argrelextrema(breath_pulse, np.less, order=10)[0]#+offset
        breath_out = argrelextrema(breath_pulse, np.greater, order=10)[0]#+offset
        self.breath = np.sort(np.hstack([breath_in, breath_out, len(self.breath_list)-1]))
          
        if self.breath[0] == breath_in[0]:
            self.btype = 'in'
        else:
            self.btype = 'out'         

        b_in = []
        b_out = []
        delidx = []

        if len(self.breath) != 0:       
            for i, j in zip(self.breath[:-1], self.breath[1:]):
                breath_diff = abs(self.breath_list[j]-self.breath_list[i])
                if abs(breath_diff) > 3000:  # really breath in/out
                    if abs(breath_diff) < 30000:  # not deep breath
                        if breath_diff > 0:  # breath out
                            print('breath out from frame '+str(i)+' to frame '+str(j)
                                +' <== breath not deep enough')
                            b_out.append(j-i)
                            self.ngframe.append(i)
                        else:  # breath in
                            print('breath in from frame '+str(i)+' to frame '+str(j)
                            +' <== breath not deep enough')
                            b_in.append(j-i)
                    else: 
                        if breath_diff > 0:  # breath out
                            print('breath out from frame '+str(i)+' to frame '+str(j))
                            b_out.append(j-i)
                        else:  # breath in
                            print('breath in from frame '+str(i)+' to frame '+str(j))
                            b_in.append(j-i)
                else:
                    delidx.append(np.argwhere(self.breath==j)[0][0])
            self.breath = np.delete(self.breath, np.array(delidx))

            print('\naverage breath out freq is: '+str(np.round(30./np.mean(b_out), 2))+' Hz')
            print('\naverage breath in freq is: '+str(np.round(30./np.mean(b_in), 2))+' Hz')
        else:
            raise ImportError('Doing too fast !! please redo again !!')

        