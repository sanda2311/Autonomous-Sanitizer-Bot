# Autonomous-Sanitizer-Bot
This robot is based on raspberry pi.
There are two file one contains the code and other is the circuit diagram of the proect.


Working of the Bot:
•	First of all check all the distances with the ultrasonic sensor and that distance will then be stored in three variables front_dist, left_dist and right_dist. Then make a decision which side to move based on the distance of obstacle returned by the ultrasonic sensor.
•	The logic for movement decision works in the following way:
If distance measured by front sensor is less than the threshold value then stop the bot, turn the servo fitted with camera in direction pointed by the front sensor and call the cam() function which takes a snapshot of the object and through image processing return whether the object is a human or not, if it is a human then another servo that is fitted with UV shield will be rotated at same angle as of the servo with the camera and if it is not a human then servo with the shield will not be rotated.

A)	Now check if the distance returned by right sensor is greater than distance returned by the left sensor if yes then there arise two condition:
1)	If the right distance is less than right threshold distance and also left distance is less than left threshold distance then for make the bot move in backwards direction until next iteration.
2)	Else move to the right direction.

B)	And if the distance of left sensor is greater than the right sensor then also there arise two condition:  
1)	If the right distance is less than right threshold distance and also left distance is less than left threshold distance then for make the bot move in backwards direction until next iteration.
2)	Else move to left direction.


•	If the front distance was not less than the threshold then we check:
A)	If left distance is less then left threshold distance then stop the bot, take a snapshot and with image processing check whether the object on the left is human or not it is human then rotate to servo of the shield towards left and if not then leave it as it is. And them rotate the bot towards right for 0.5 sec and run next iteration.
B)	Else If right distance is less then right threshold distance then stop the bot, take a snapshot and with image processing check whether the object on the right is human or not it is human then rotate to servo of the shield towards right and if not then leave it as it is. And them rotate the bot towards left for 0.5 sec and run next iteration.
•	If none of the condition holds true then keep moving forward.

If CTRL+C is pressed then signal on all the pins GPIO pins will be cleared and the program will terminate.

