import datetime


class Kparam(object):
    """ Kinect intervention project parameters' initialization 
    """

    def __init__(self,exeno='', username=''):

        self.bdjoints   = []
        self.now  = datetime.datetime.now() 
        self.dstr = './output/'+username+'data'+repr(self.now.year)+repr(self.now.month).zfill(2)\
                               +repr(self.now.day).zfill(2)+repr(self.now.hour).zfill(2)\
                               +repr(self.now.minute).zfill(2)+repr(self.now.second).zfill(2)+str(exeno)
        self.scale       = 1.0
        self.scene_type  = 2
        self.pre_scale   = 1.0  
        self.ini_scale   = 1.0
        self.ratio       = 0.5  # propotion of avatar and color frame
        self._done       = False
        self.finish      = False
        self.handmode    = False
        self.vid_rcd     = False
        self.model_draw  = False
        self.model_frame = False
        self.clipNo      = 0
        self.fno         = 0 
        self.framecnt    = 0

        # === Font setting ===
        # color
        # instruction part
        self.c_inst = (0, 90, 115, 255)
        self.c_tips = (19, 144, 178, 0)
        # eval part
        self.c_guide     = (0, 90, 115, 255)
        self.c_eval_well = (19, 144, 178, 0)
        self.c_eval_err  = (230, 115, 0, 255)
        self.c_togo      = (255, 20, 100, 255)
        # style
        self.s_normal = 'montserrat'
        self.s_emp = 'montserrat'
        self.eval_fs_title = 100
        self.eval_fs_guide = 80
        self.eval_fs_msg = 70
        self.eval_fs_cnt = 100
        self.inst_size = 40
        #  === UI setting  ===
        #  (based on 1920*1080 setting)
        self.eval_LB = 120  # evaluation Left bound
        self.eval_RB = 980  # evaluation Right bound
        self.video_LB = 1080  # video Left bound
        self.video_RB = 1830  # video Right bound
        # video size 750*420
        self.vid_w = 750
        self.vid_h = 420
        self.video1_UB = 110  # video1 upper bound
        self.video2_UB = 560  # video2 upper bound
        # eval sections
        self.eval_sec1 = 110
        self.eval_sec2 = 330
        self.eval_sec3 = 455
        self.eval_sec4 = 835
        self.eval_sec5 = 900
        self.eval_sec6 = 1080
        self.eval_sec = [self.eval_sec1, self.eval_sec2, self.eval_sec3,
                         self.eval_sec4, self.eval_sec5, self.eval_sec6]



                  




