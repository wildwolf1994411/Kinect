

class Kinect_para(object):
    """ define some KinectV2 pre-assign parameters
    """
    def __init__(self):
        # joint order in kinect
        self.JointType_SpineBase     = 0
        self.JointType_SpineMid      = 1
        self.JointType_Neck          = 2
        self.JointType_Head          = 3
        self.JointType_ShoulderLeft  = 4
        self.JointType_ElbowLeft     = 5
        self.JointType_WristLeft     = 6
        self.JointType_HandLeft      = 7
        self.JointType_ShoulderRight = 8
        self.JointType_ElbowRight    = 9
        self.JointType_WristRight    = 10
        self.JointType_HandRight     = 11
        self.JointType_HipLeft       = 12
        self.JointType_KneeLeft      = 13
        self.JointType_AnkleLeft     = 14
        self.JointType_FootLeft      = 15
        self.JointType_HipRight      = 16
        self.JointType_KneeRight     = 17
        self.JointType_AnkleRight    = 18
        self.JointType_FootRight     = 19
        self.JointType_SpineShoulder = 20
        self.JointType_HandTipLeft   = 21
        self.JointType_ThumbLeft     = 22
        self.JointType_HandTipRight  = 23
        self.JointType_ThumbRight    = 24
        self.JointType_Count         = 25

        # values for enumeration '_TrackingState'
        self.TrackingState_NotTracked = 0
        self.TrackingState_Inferred   = 1
        self.TrackingState_Tracked    = 2

        # upperbody index
        self.SpineBase_x   = 0
        self.SpineBase_y   = 1
        self.SpineBase_z   = 2
        self.SpineMid_x    = 3
        self.SpineMid_y    = 4
        self.SpineMid_z    = 5
        self.Neck_x        = 6
        self.Neck_y        = 7
        self.Neck_z        = 8
        self.Head_x        = 9
        self.Head_y        = 10
        self.Head_z        = 11
        self.LShld_x       = 12
        self.LShld_y       = 13
        self.LShld_z       = 14
        self.LElbow_x      = 15
        self.LElbow_y      = 16
        self.LElbow_z      = 17
        self.LWrist_x      = 18
        self.LWrist_y      = 19
        self.LWrist_z      = 20        
        self.RShld_x       = 21
        self.RShld_y       = 22
        self.RShld_z       = 23
        self.RElbow_x      = 24
        self.RElbow_y      = 25
        self.RElbow_z      = 26
        self.RWrist_x      = 27
        self.RWrist_y      = 28
        self.RWrist_z      = 29
        self.SpineShld_x   = 30
        self.SpineShld_y   = 31
        self.SpineShld_z   = 32




