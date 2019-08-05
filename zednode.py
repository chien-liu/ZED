#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
import cv2

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from zedcv2 import Camera


while(True):
    # Capture frame-by-frame
    frame = zed.retrieve_image()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

class image_converter:

    def __init__(self):
        # ROS
        self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.bridge = CvBridge()
        # zedcv2
        self.zed = Camera()
        self.zed.set_resolution("2K")    # "2K", "1080p", "720p", "WVGA"
        self.zed.set_eye("left")         # "left", "right", "both"

    def get_image(self):
        # Capture frame-by-frame
        cv2_image = zed.retrieve_image()
        self.callback(cv2_image)

    def callback(self, cv2_image)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv2_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

def main(args):
    ic = image_converter()
    
    rospy.init_node('zedcv2_raw_image', anonymous=True)

    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        ic.get_image()
        r.sleep()


if __name__ == '__main__':
    main(sys.argv)