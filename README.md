# Game

Aidan, could you just look at the collision function and figure out why it won't work please. 

You should be allowed to move one circle around with WASD.

The collision function should stop the two circles from over lapping but that is really buggy and I just can't tell why, I think a fresh pair of eyes would help. I'll explain how it works below.

The wall's x and y coords are stored in self.pos.
The player's are stored as x and y in this function.
It find the distance between them by the pythagorean therom.
If that is less than 100 then it run the following code.
It finds the angle between the line (from the object to the player) and the y axis.
It then finds the x and y components of the triangle made from theta and the radius.
It adds 50 to them because pygame's sprite positioning is not centre aligned.
It then returns the values to be the player's x and y values

Below is a bad diagram of what I was trying to explain above:

https://share.icloud.com/photos/01cSgje5dgR_79dPP1IjQvJ3Q 
