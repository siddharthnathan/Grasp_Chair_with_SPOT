# Import Necessary SPOT Scripts
from spot_robot import make_SPOT_stand
from spot_robot import DetectFiducial
import bosdyn

# Import Necessary Scripts
import read_video_stream
import pose_estimation
import coordinate_transformations
import utils

# Import Necessary Libraries
import numpy as np
import time
import cv2
import os


# Define a Function to Setup and Configure SPOT Robot
def setup_and_configure_robot():

    # Define the SPOT Robot Credentials
    os.environ['BOSDYN_CLIENT_USERNAME'] = "admin"
    os.environ['BOSDYN_CLIENT_PASSWORD'] = "pvwmr4j08osj"
    robot_ip = "192.168.80.3"

    # Setup Configurations for SPOT
    bosdyn.client.util.setup_logging(False)
    sdk = bosdyn.client.create_standard_sdk('WalkToObjectClient')
    robot = sdk.create_robot(robot_ip)
    bosdyn.client.util.authenticate(robot)
    robot.time_sync.wait_for_sync()

    # Return the Robot object
    return robot


# Define the type of AruCo marker used in Environment
aruco_type = cv2.aruco.DICT_APRILTAG_36h11

# Read Camera Calibration parameters
camera_calibration_params = utils.read_camera_calibration_params()
'''
# Configure and Stream Realsense Pipeline
main_camera_pipeline = read_video_stream.configure_and_stream_pipeline()

# Configure SPOT robot and make it Stand
robot = setup_and_configure_robot()
make_SPOT_stand(robot)

# Read Image frames from both the Cameras
try:

    # Read Image frames continuously
    while True:
        
        # Read Image frames from Pipelines
        main_camera_frame = read_video_stream.read_frames_from_pipelines(main_camera_pipeline)
        
        # Get the Pose of AruCo tags in Main Camera frame
        image_with_aruco_poses, aruco_tags_data_wrt_camera_frame = pose_estimation.get_pose_of_aruco_tags(main_camera_frame, aruco_type, camera_calibration_params['Main_Camera'])

        # Detect the Fiducials in the Robot's environment
        aruco_tags_data_wrt_spot_body_frame = DetectFiducial(robot).detect_aruco_tags_wrt_spot_body_frame()

        # Create Object list for AruCo tags data in Main camera frame and SPOT frame
        aruco_tags_data_wrt_camera_frame = coordinate_transformations.create_coordinate_frames(aruco_tags_data_wrt_camera_frame, 'Camera')
        aruco_tags_data_wrt_spot_frame = coordinate_transformations.create_coordinate_frames(aruco_tags_data_wrt_spot_frame, 'SPOT')

        # If Chair is Detected in Camera and SPOT frames
        if utils.is_aruco_detected(aruco_tags_data_wrt_camera_frame, 'Chair') or utils.is_aruco_detected(aruco_tags_data_wrt_spot_frame, 'Chair'):
            print("Y")

        # If Chair is not Detected in Camera and SPOT frames
        else:
            print("Chair is Not detected in Camera & SPOT frames")

        # Display the Image from Main Camera
        cv2.imshow('Main_Camera', image_with_aruco_poses)
        cv2.waitKey(1)
        time.sleep(5)

        # Quit when Q key is Pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Stop streaming finally
finally:
    main_camera_pipeline.stop()


'''
# Read Image frames from Pipelines
main_camera_frame = cv2.imread('scene.jpg')
        
# Get the Pose of AruCo tags in Main Camera frame
image_with_aruco_poses, aruco_tags_data_wrt_camera_frame = pose_estimation.get_pose_of_aruco_tags(main_camera_frame, aruco_type, camera_calibration_params['Main_Camera'])
    
aruco_tags_data_wrt_spot_frame = [{'Name': 'Main_Origin', 'Translation': [-3.799, -1.197, 0.341], 'Rotation': [24.448, 78.03, -115.392]}, 
                      {'Name': 'Secondary_Origin', 'Translation': [0.83, -1.929, 0.296], 'Rotation': [2.144, -18.248, -89.994]}]

# Create Object list for AruCo tags data in Main camera frame and SPOT frame
aruco_tags_data_wrt_camera_frame = coordinate_transformations.create_coordinate_frames(aruco_tags_data_wrt_camera_frame, 'Camera')
aruco_tags_data_wrt_spot_frame = coordinate_transformations.create_coordinate_frames(aruco_tags_data_wrt_spot_frame, 'SPOT')

# Define Main Origin Pose wrt Camera frame
main_origin_pose_wrt_camera_frame = utils.get_aruco_tag_data(aruco_tags_data_wrt_camera_frame, 'Main_Origin')

# Define Secondary Origin Pose wrt Camera frame
secondary_origin_pose_wrt_camera_frame = utils.get_aruco_tag_data(aruco_tags_data_wrt_camera_frame, 'Secondary_Origin')

# If Chair is Detected in Camera and SPOT frames
if utils.is_aruco_detected(aruco_tags_data_wrt_camera_frame, 'Chair') or utils.is_aruco_detected(aruco_tags_data_wrt_spot_frame, 'Chair'):

    # If Chair is detected by SPOT
    if utils.is_aruco_detected(aruco_tags_data_wrt_spot_frame, 'Chair'):

        # Get the Pose of AruCo on Chair wrt SPOT body frame
        chair_aruco_pose_wrt_spot_frame = utils.get_aruco_tag_data(aruco_tags_data_wrt_spot_frame, 'Chair')
    
    # Else when Chair is not detected by SPOT and only Camera
    else:

        # Compute the Pose of AruCo on Chair wrt SPOT body frame
        chair_aruco_pose_wrt_spot_frame = coordinate_transformations.compute_chair_pose_wrt_spot(aruco_tags_data_wrt_camera_frame, aruco_tags_data_wrt_spot_frame)
        print(chair_aruco_pose_wrt_spot_frame)

# If Chair is not Detected in Camera and SPOT frames
else:
    print("Chair is Not detected in Camera & SPOT frames")

cv2.imshow('Main_Camera', image_with_aruco_poses)
cv2.waitKey(0)
