[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AktWbCri)
# assignment-04-CV-Sensor-Fusion

## Perspective Transformation
start the script with command like: `python image_extractor.py sample_image.jpg cutout.jpg, 500, 500`, then
follow the instructions on the command line

call paramters: input path, output path, result resolution value 1, result resolution value 2

## AR Game
- navigate to the `ar_game` folder and start the script with `python AR_game.py`
- hold the board with the aruco markers out in front of you so the markers 1 and 3 are at the top and facing the camera.
(if you are not sure which markers are 1 and 3, check out this website: https://chev.me/arucogen/ (look at 6x6 and the desired ID))
- make sure all 4 markers are in the camera frame, so they can get recognized. Once they are, the game starts.
- The goal is to destroy as many bricks as you can by bouncing the ball off the paddle at the bottom. You can move the paddle by inserting your finger or another dark object like a pen from the bottom and moving it side to side

## Sensor Fusion
- navigate to the sensor_fusion folder and start the script with `python sensor_fusion.py`
- hold the board with the aruco markers out in front of you so the markers 1 and 3 are at the top and facing the camera.
(if you are not sure which markers are 1 and 3, check out this website: https://chev.me/arucogen/ (look at 6x6 and the desired ID))
- make sure all 4 markers are in the camera frame, so they can get recognized. Once they are, you can see the transformed rectangle
-move marker 5 in the region between the other markers (I found it easiest to stick it to the end of a think stick to not cover the other markers when moving)