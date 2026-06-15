import cv2
import sys
import numpy as np

source_path = sys.argv[1:][0]
save_path = sys.argv[1:][1]
result_resolution_1 = sys.argv[1:][2]
result_resolution_2 = sys.argv[1:][3]

print(f"result resolution: {result_resolution_1}, {result_resolution_2}")
original_img = cv2.imread(source_path)
img = original_img.copy() 

WINDOW_NAME = 'Awesome Window'

cv2.namedWindow(WINDOW_NAME)

#count clicks
counter = 0
#positions of clicked points
points = [[0,0], [0,0], [0,0], [0,0]]

def mouse_callback(event, x, y, flags, param):
    global img, counter, points

    if event == cv2.EVENT_LBUTTONDOWN and counter < 4:
        img = cv2.circle(img, (x, y), 5, (255, 0, 150), -1)
        points[counter] = [x,y]
        cv2.imshow(WINDOW_NAME, img)
        counter += 1
        if counter == 4:
            transform_cutout()

def transform_cutout():
    global img, counter, save_path, result_resolution_1, result_resolution_2, points
    print("transformers are awsome")
    points = np.float32(points)
    points_2 = np.float32([[0,0],[int(result_resolution_1),0],[int(result_resolution_1),int(result_resolution_2)], [0,int(result_resolution_2)]])

    M = cv2.getPerspectiveTransform(points, points_2)

    img = cv2.warpPerspective(img, M, (int(result_resolution_1), int(result_resolution_2)))

    print("cutout created. Press esc or q to go back or s to save your cutout")

    while True:
        cv2.imshow(WINDOW_NAME, img)

        key = cv2.waitKey(0)

        if key == ord('q') or key == 27:#esc
            counter = 0
            img = original_img.copy()
            points = [[0,0], [0,0], [0,0], [0,0]]
            cv2.imshow(WINDOW_NAME, img)
            return
        elif key == ord('s'):
            (cv2.imwrite(save_path, img))
            print("cutout saved")

print("window started. click 4 points clockwise, starting from the top left, to mark your desired cutout\nQ to close the window\nESC to delete the selected points\nS to save the cutout")
while True:
    cv2.imshow(WINDOW_NAME, img)

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    key = cv2.waitKey(0)
    if key == ord('q'):
        print("window closed")
        break
    elif key == 27:#esc
        counter = 0
        img = original_img.copy()
        points = [[0,0], [0,0], [0,0], [0,0]]
        print("points deleted. If you wanted to close the window, press 'q' instead")
    elif key == ord('s'):
        print("no cutout image to save yet")
