import pyzed.sl as sl


def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.sdk_verbose = False

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Error")
        exit(1)

    # Get camera information (ZED serial number)
    zed_serial = zed.get_camera_information().serial_number
    print("Hello! This is my serial number: {0}".format(zed_serial))

    # Get camera information (fx, fy, cx, cy)
    calibration_params = zed.get_camera_information().calibration_parameters
    print("Left cam:")
    focal_left_x = calibration_params.left_cam.fx   # Focal length of the left eye in pixels
    focal_left_y = calibration_params.left_cam.fy
    optical_center_left_x = calibration_params.left_cam.cx  # Optical center along x axis, defined in pixels (usually close to width/2).
    optical_center_left_y = calibration_params.left_cam.cy
    print("fx: {}\nfy: {}\ncx: {}\ncy: {}".format(focal_left_x, focal_left_y, optical_center_left_x, optical_center_left_y))
    print("Right cam:")
    focal_right_x = calibration_params.right_cam.fx   # Focal length of the left eye in pixels
    focal_right_y = calibration_params.right_cam.fy
    optical_center_right_x = calibration_params.right_cam.cx  # Optical center along x axis, defined in pixels (usually close to width/2).
    optical_center_right_y = calibration_params.right_cam.cy
    print("fx: {}\nfy: {}\ncx: {}\ncy: {}".format(focal_right_x, focal_right_y, optical_center_right_x, optical_center_right_y))

    

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()