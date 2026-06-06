import cv2

img = cv2.imread('sample_image.jpg')
WINDOW_NAME = 'Awesome Window'

cv2.namedWindow(WINDOW_NAME)

#count clicks
counter = 0

def mouse_callback(event, x, y, flags, param):
    global img, counter

    if event == cv2.EVENT_LBUTTONDOWN:
        img = cv2.circle(img, (x, y), 5, (255, 0, 150), -1)
        cv2.imshow(WINDOW_NAME, img)
        counter += 1
        if counter == 4:
            transform_cutout()

def transform_cutout():
    global img, counter
    print("transformers are awsome")
    #TODO
    #transformation
    #s to save (cv2.imwrite('name', img))
    ...

while True:
    cv2.imshow(WINDOW_NAME, img)

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    if key == ord('esc'):
        counter = 0
        #fixme delete points
