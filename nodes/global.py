import rospy
from rospy.msg import XXX
import numpy as np

class GlobalTransformer:

    def __init__(self):
        self.attitudeSubscriber = rospy.Subscriber('attitude', TYPE, attitudeCallback)
        # quaternion expressed as [w,x,y,z]
        self.attitude = np.array([0,0,0,0])

        self.positionSubscriber = rospy.Subscriber('position', TYPE,  positionCallback)
        # vector expressed as [x,y,z]
        self.position = np.array([0,0,0])

    def rotationMatrix(self):
        w, x, y, z = self.attitude
        R = np.zeros((3,3))
        R[0,0] = 1 - 2*y**2 - 2*z**2
        R[0,1] = 2*x*y-2*z*w
        R[0,2] = 2*x*z + 2*y*w
        R[1,0] = 2*x*y + 2*z*w
        R[1,1] = 1 - 2*x**2 - 2*z**2
        R[1,2] = 2*y*z - 2*x*w
        R[2,0] = 2*x*z - 2*y*w
        R[2,1] = 2*y*z + 2*x*w
        R[2,2] = 1 - 2*x**2 - 2*y**2
        return R

    def transformMatrix(self):
        M = np.zeros((4,4))
        R = self.rotationMatrix(self.attitude)
        M[:3, :3] = R
        M[:3, 3] = self.position.T
        M[3,3] = 1
        return M

    def attitudeCallback(self, attitude):
        self.attitude = attitude

    def positionCallback(self, position):
        self.position = position

class CircleTransformer:

    def __init__(self, globalTransformer):
        self.globalTransformer = globalTransformer
        self.circleSubscriber = rospy.Subscriber('circles', TYPE, self.callback)
        self.circlePublisher = rospy.Publisher('globalCircles', TYPE)

    def callback(self, circles):
        M = self.globalTransformer.transformMatrix()
        globalCircles = []
        for c in circles:
            gc = np.multiply(M, c)
            globalCircles.append(gc)
        self.circlePublisher.publish(globalCircles)

class LineTransformer:

    def __init__(self, globalTransformer):
        self.globalTransformer = globalTransformer
        self.lineSubscriber = rospy.Subscriber('lines', TYPE, self.callback)
        self.linePublisher = rospy.Publisher('globalLines', TYPE)

    def callback(self, lines):
        M = self.globalTransformer.transformMatrix()
        globalLines = []
        for (pt1, pt2) in lines:
            gpt1 = np.multiply(M, pt1)
            gpt2 = np.multiply(M, pt2)
            globalLines.append((gpt1, gpt2))
        self.linePublisher.publish(globalLines)


if __name__ == '__main__':
    rospy.init():
    globalTransformer = GlobalTransformer()
    circleTransformer = CircleTransformer(globalTransformer)
    lineTransformer = LineTransformer(globalTransformer)
