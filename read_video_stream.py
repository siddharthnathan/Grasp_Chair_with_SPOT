# Import Necessary Libraries
import pyrealsense2 as rs
import numpy as np
import cv2


# Define a Function to Configure and Stream Realsense Pipeline using Cameras
def configure_and_stream_pipeline():

    # Exit if the Number of Cameras are less than 2
    devices = rs.context().devices
    if len(devices) < 1:
        print("Not enough cameras connected.")
        exit()
    
    # If there are 2 cameras connected
    else:

        # Initialise Pipelines for Cameras
        pipelines = []

        # For every Device connected
        for device in devices:

            # Configure the RealSense pipeline
            pipeline = rs.pipeline()
            config = rs.config()

            # Enable the Camera streams
            config.enable_device(device.get_info(rs.camera_info.serial_number))
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            # Start streaming
            pipeline.start(config)
            pipelines.append(pipeline)
        
        # Extract Pipelines for Main camera and Side camera
        main_camera_pipeline = pipelines[0]

        # Return the Pipelines
        return main_camera_pipeline


# Define a Function to Read Image frames from Pipelines
def read_frames_from_pipelines(main_camera_pipeline):

    # Get Frames from Main camera
    main_camera_frame = main_camera_pipeline.wait_for_frames()
    main_camera_frame = main_camera_frame.get_color_frame()
    main_camera_frame = np.asanyarray(main_camera_frame.get_data())

    # Display the images
    cv2.imshow('Main_Camera', main_camera_frame)

    # Return the Image frames
    return main_camera_frame