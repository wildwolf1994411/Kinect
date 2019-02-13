
class Kinect_data_3D(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class Kinect_2D_pts(object):

    def __init__(self):
        self.x = 0
        self.y = 0


class Kinect_3D_pts(Kinect_data_3D):

    def __init__(self):
        self.Position = Kinect_data_3D()
        self.JointType = 0
        self.TrackingState = 0