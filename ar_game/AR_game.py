import cv2
import cv2.aruco as aruco
import sys
import numpy as np
import pyglet
from pyglet import window, shapes, font
from PIL import Image
import sys
import random
import time

#load cool font (https://www.1001fonts.com/pixel-game-font.html)
font.add_file('Pixel Game.otf')

#global variables
markers_detected = False
end = False
score = 0

#video source
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

win = window.Window(width, height, caption="Cool Video Game")

#shapes for the game
#paddle
paddle_width = max(width/10, 20)
paddle_height = max(height/40, 5)

paddle = shapes.Rectangle(width//2 - paddle_width//2,
                          paddle_height,
                          paddle_width,
                          paddle_height,
                          color = (0, 255, 0))

#ball
ball_radius = paddle_width/4

ball = shapes.Circle(width//2, 
                     height//2,
                     ball_radius,
                     color=(255, 0, 0))

#speed in x and y direction
ball_vx = 8
ball_vy = 8

#bricks
bricks = []

rows = 5
cols = 10

brick_width = width / 15
brick_height = paddle_height

for row in range(rows):
    for col in range(cols):
        brick = shapes.Rectangle(
            brick_width + col * (brick_width + 1/3 * brick_width),
            height - 2 * brick_height - row * (brick_height + 1/3 * brick_width),
            brick_width,
            brick_height,
            color=(
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255),
            )
        )
        bricks.append(brick)

#Reset button on end screen
reset_button = shapes.Rectangle(
    width//2 - 100,
    height//2 - 75,
    200,
    50,
    color=(50, 150, 50)
)

reset_label = pyglet.text.Label(
    "Play Again",
    font_name='Pixel Game',
    font_size=20,
    x=width//2,
    y=height//2 - 50,
    anchor_x="center",
    anchor_y="center"
)

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

#get mask for objects in the foreground, assuming the background is close to white
def get_mask(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    #remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask

#extract contour of object from background with mask
def get_object_contour(mask):
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    return max(contours, key=cv2.contourArea)

#get position of tip (smallest y value)
def get_tip(contour):
    points = contour[:, 0, :]

    tip = points[np.argmin(points[:, 1])]

    return tuple(tip)


#reset game to start parameters
def reset_game():
    global end, score, ball, ball_vx, ball_vy, bricks, rows, cols, brick_width, brick_height

    end = False
    score = 0

    ball.x = width // 2
    ball.y = height // 2

    ball_vx = 8
    ball_vy = 8

    bricks = []

    for row in range(rows):
        for col in range(cols):
            brick = shapes.Rectangle(
                brick_width + col * (brick_width + 1/3 * brick_width),
                height - 2 * brick_height - row * (brick_height + 1/3 * brick_width),
                brick_width,
                brick_height,
                color=(
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                )
            )
            bricks.append(brick)

    end = False

#reset game when reset button is pressed
@win.event
def on_mouse_press(x, y, button, modifiers):
    if not end:
        return

    if (reset_button.x <= x <= reset_button.x + reset_button.width
        and reset_button.y <= y <= reset_button.y + reset_button.height):
        reset_game()



@win.event
def on_draw():
    global markers_detected, end, ball_vx, ball_vy, score

    if not end: 


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
                #start transformation if all 4 markers are successfully captured
                if len(ids) == 4:
                    markers_detected = True
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

                    #inner corners of all 4 markers
                    points = np.float32(points)
                    #their position on the transformed frame
                    points_2 = np.float32([[0, height], [0, 0], [width, height], [width, 0]])

                    #transform frame to display the rectangle between the markers with camera's resolution
                    M = cv2.getPerspectiveTransform(points, points_2)
                    frame = cv2.warpPerspective(frame, M, (width, height))

                    #finger detection
                    mask = get_mask(frame)
                    contour = get_object_contour(mask)
                    if contour is not None:
                        tip = get_tip(contour)
                        x,y = tip

                        #game mechanics
                        #paddle follows finger
                        paddle.x = x - paddle_width/2
                        paddle.x = max(0, min(width - paddle_width, paddle.x))

                        #ball movement
                        ball.x += ball_vx
                        ball.y += ball_vy

                        #wall collision
                        if ball.x - ball.radius <= 0:
                            ball.x = ball.radius
                            ball_vx *= -1

                        if ball.x + ball.radius >= width:
                            ball.x = width - ball.radius
                            ball_vx *= -1

                        if ball.y + ball.radius >= height:
                            ball.y = height - ball.radius
                            ball_vy *= -1

                        #ball lost
                        if ball.y < 0:
                            end = True

                        #paddle collision
                        if (
                            ball.y - ball.radius <= paddle.y + paddle.height
                            and paddle.x <= ball.x <= paddle.x + paddle.width
                            and ball_vy < 0
                        ):
                            ball_vy = abs(ball_vy)

                            #add angle depending on hit position
                            offset = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2)
                            ball_vx += offset * 15

                        #brick collision
                        hit_brick = None

                        for brick in bricks:
                            if (brick.x <= ball.x <= brick.x + brick.width
                                and brick.y <= ball.y <= brick.y + brick.height):
                                hit_brick = brick
                                score += 1
                                break

                        if hit_brick:
                            bricks.remove(hit_brick)
                            ball_vy *= -1
                            if len(bricks) == 0:
                                end = True

                else:
                    markers_detected = False

            # Display the frame
            win.clear()
            img = cv2glet(frame, 'BGR')
            img.blit(0, 0, 0)

            if markers_detected:
                paddle.draw()
                ball.draw()
                for brick in bricks:
                    brick.draw()
                    
                #label to show current score
                label_score = pyglet.text.Label(f'Score: {score}',
                                                font_name='Pixel Game',
                                                font_size=36,
                                                color = (0, 0, 0),
                                                x=10, y=10)
                label_score.draw()

    #end = True, ball got lost or all bricks were destroyed        
    else:
        win.clear()
        if len(bricks) == 0:
            txt = "Congratulations, you got them all!"
        else: 
            txt = f'Game Over!  Score: {score}'

        label_end = pyglet.text.Label(txt,
                            font_name='Pixel Game',
                            font_size=36,
                            x=width/2,
                            y=height/2 + 50,
                            anchor_x = "center",
                            anchor_y = "center")
        label_end.draw()
        reset_button.draw()
        reset_label.draw()

pyglet.app.run()
