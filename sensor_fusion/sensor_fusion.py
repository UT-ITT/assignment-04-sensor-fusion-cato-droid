import cv2
import cv2.aruco as aruco
import sys
import numpy as np
import pyglet
from pyglet import window, shapes
from PIL import Image
import sys

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# Define the ArUco dictionary, parameters, and detector
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
aruco_params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, aruco_params)

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
win = window.Window(width, height, caption="Sensor Fusion")

#red dot to track the aruco marker with ID 5
tracker_radius = width // 30
tracker = shapes.Circle(0, 
                        0,
                        tracker_radius,
                        color=(255, 0, 0))

# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img,fmt):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape
    raw_img = Image.fromarray(img).tobytes()
    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg

@win.event
def on_draw():
    #global width, height
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if ret:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect ArUco markers in the frame
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        # Check if marker is detected
        if ids is not None:
            # Draw lines along the sides of the marker
            aruco.drawDetectedMarkers(frame, corners)
            marker_5_point = np.array([[[0, 0]]], dtype="float32")
            #start transformation if all 4 markers are successfully captured
            if len(ids) >= 4:
                points = [[0,0], [0,0], [0,0], [0,0]]
                #order marker points to put the correct corner values in points for the transition to work
                for i in range (len(ids)):
                    if ids[i] == [0]:
                        points[0] = corners[i][0][3]
                    elif ids[i] == [1]:
                        points[1] = corners[i][0][0]
                    elif ids[i] == [2]:
                        points[2] = corners[i][0][2]
                    elif ids[i] == [3]:
                        points[3] = corners[i][0][1]

                    #track 5th marker (ID 5) and put tracker over its position
                    elif ids[i] == [5]:
                        ll = corners[i][0][0]
                        lr = corners[i][0][1]
                        ur = corners[i][0][2]
                        ul = corners[i][0][3]
                        marker_5_x = (lr[0] + (ll[0] - lr[0]) / 2)
                        marker_5_y = (ur[1] + (lr[1] - ur[1]) / 2)
                        marker_5_point = np.array([[[marker_5_x, marker_5_y]]], dtype="float32")

                #inner corners of all 4 markers
                points = np.float32(points)
                #their position on the transformed frame
                points_2 = np.float32([[0, height], [0, 0], [width, height], [width, 0]])
                #transform frame to display the rectangle between the markers with camera's resolution
                M = cv2.getPerspectiveTransform(points, points_2)
                frame = cv2.warpPerspective(frame, M, (width, height))
                #also transform coordinates of marker 5 for tracker
                marker_5_transformed = cv2.perspectiveTransform(marker_5_point, M)
                tracker.x = marker_5_transformed[0][0][0]
                tracker.y = height - marker_5_transformed[0][0][1]

        # Display the frame
        win.clear()
        img = cv2glet(frame, 'BGR')
        img.blit(0, 0, 0)
        tracker.draw()

pyglet.app.run()