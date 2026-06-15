[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AktWbCri)
# assignment-04-CV-Sensor-Fusion

## Perspective Transformation
start the script with command like: `python image_extractor.py sample_image.jpg cutout.jpg 500 500`, then
follow the instructions on the command line

call paramters: input path, output path, result resolution value 1, result resolution value 2

## AR Game
- navigate to the `ar_game` folder and start the script with `python AR_game.py`
- hold the board with the aruco markers out in front of you so the markers 1 and 3 are at the top and facing the camera.
(if you are not sure which markers are 1 and 3, check out this website: https://chev.me/arucogen/ (look at 6x6 and the desired ID))
- make sure all 4 markers are in the camera frame, so they can get recognized. Once they are, the game starts.
- The goal is to destroy as many bricks as you can by bouncing the ball off the paddle at the bottom. You can move the paddle by inserting your finger or another dark object like a pen from the bottom and moving it side to side

## Sensor Fusion
- start the DIPPID app and set the IP to your computer's IP in the same network as your phone
- navigate to the sensor_fusion folder and start the script with `python sensor_fusion.py`
- hold the board with the aruco markers out in front of you so the markers 1 and 3 are at the top and facing the camera.
(if you are not sure which markers are 1 and 3, check out this website: https://chev.me/arucogen/ (look at 6x6 and the desired ID))
- make sure all 4 markers are in the camera frame, so they can get recognized. Once they are, you can see the transformed rectangle
- move your phone with marker 5 in the region between the other markers. You can now see the tracker tracking the marker (red) and the prediction based on the accelerometer data (green)
- To adjust the alpha value, use the arrow keys: up/right: increase alpha by 0.1 (until 1), down/left: decrease alpha by 0.1 (until 0)
- to reset the prediction to the tracker position, press button 1 in your DIPPID app

Zur Implementation: 
Ich habe Code aus Aufgabe 2 und den Übungen aus der Vorlesung wiederverwendet und dann versucht so anzupassen, dass eine sinnvolle Vorhersage bei rum kommt. Leider Habe ich es in meinem Versuchsaufbau nicht ganz hinbekommen. Bei der Größe des boards im Verhältnis zum Handy ist nicht viel/schnelle Bewegung möglich, sodass die Accelerometer Daten die ich bekommen habe von noise dominiert waren. Also bevor ich den Skalierungsfaktor so weit erhöhen konnte, dass man tatsächlich hätte eine sinnvolle Vorhersage im Bild hätte erkennen können, ist durch das noise ein so starker sensor drift entstanden, dass die Vorhersage auch ohne Bewegung schon recht weit vom tracker entfernt war. Wenn ich die Geschwindigkeit kontinuierlich aufaddiere, entfernt sich die prediction kontinulierlich vom Tracker. Wenn ich sie bei jedem Schritt komplett neu berechne, kann ich den Skalierungsfaktor deutlich höher wählen, aber bekomme dann einen statisch großen Abstand zum Tracker, der kaum durch die eigentliche Bewegung vom Handy beeinflusst wird (viel mehr noise als eigentlich interessante Daten :( ). Vielleicht hab ich hier auch bei der Berechnung einen Fehler gemacht, aber ich weiß nicht wirklich wo, da ich ja nur die Accelorometer Daten die ich bekomme stärker oder weniger stark gewichten kann, aber die schon so viel noise enthalten, das ich nicht hinbekommen habe rauszufiltern. 
Zusätzlich ist mein Rechner auch noch recht langsam, sodass die Berechnung der Prediction immer ein kleines bisschen länger dauert als die für den Tracker. Es entsteht also bei mir wenn ich das Handy bewege der Effekt, dass die Prediction sogar hinter den eigentlichen Tracker hinterher hinkt. 
Die alpha-Werte habe ich nach meinem Verständnis aus der Vorlesung dazuaddiert (also bei kleinem alpha ist der eine Teil der Fusion wichtiger, bei großem alpha der andere Teil). Hier konnte ich feststellen, dass je höher das alpha ist, desto größer auch der sensor drift (also das Abweichen der prediction vom tracker) ist, was auch Sinn macht, da bei größerem alpha die Accelorometer-Daten einen größeren Effekt haben. 