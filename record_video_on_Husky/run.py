import sys, os
import copy
from datetime import datetime
import time
import logging
from argparse import ArgumentParser
import numpy as np
import pyzed.sl as sl

# ROS path disturb import cv2
try:
    sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
except:
    pass

import cv2


parser = ArgumentParser()
parser.add_argument("-f", "--fps", type=float, default=2,
                    help="Frame per second. type: int. Maximun Value: 1080P-->30fps, 2.2K-->15fps.")
parser.add_argument("-e", "--exposure", type=int, default=-1,
                    help="Exposure time. Value from 0 to 100. The larger, the brighter for images.")
parser.add_argument("--no-save", action="store_true",
                    help="Not storing vidoe. This flag is for debugging")
parser.add_argument("--no-show", action="store_true",
                    help="Not steaming.")

args = parser.parse_args()


def main():
    # create directory with name base on system time
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    if not args.no_save:       
        if os.path.isdir(timestamp):
            assert False, "Directory exist"
        os.mkdir(timestamp)

        ith_image = 0

    # Create a Camera object
    zed = sl.Camera()
    

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD2K  # Use HD2K video mode
    init_params.camera_fps = 15
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_NONE


    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Error: Can't connect to ZED.")
        exit(1)
    if args.exposure == -1:
        # Reset to auto exposure
        zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE, -1, True)
        print("Setting camera to auto exposure.")
    else:
        zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE, args.exposure, False)  # Set shutter time to the minimum value 0.17072ms.
        print("CAMERA_SETTINGS_EXPOSURE:", zed.get_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE))

    
    # while loop
    image = sl.Mat()
    depth_map = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    while True:
        time.sleep(1/args.fps)  # Set fps at 2  (max: 15)
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
            zed.retrieve_measure(depth_map, sl.MEASURE.MEASURE_DEPTH) # Retrieve depth
            
            # save image
            if not args.no_save:
                cv2.imwrite("./{}/{}.png".format(timestamp, ith_image), image.get_data())

                ith_image += 1
                
            # show image
            if not args.no_show:
                cv2.imshow("image", image.get_data())
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

if __name__ == "__main__":
    main()
