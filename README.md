# Game
This is an old project of mine, hence why the code and repository are unorganised. This is also true for a lot of the projects on here

The premise is you have three boomerangs and have to take out enemies to get to the next level.

# Controls

wasd or arrow keys to move
Left click to throw
Right click to catch

# Links

I can't be bothered to copy all the images over right now so here's links to their folders. 

https://replit.com/@andel252/Adventure-trial#buttons
https://replit.com/@andel252/Adventure-trial#images

Also here's a link to the replit page:
https://replit.com/@andel252/Adventure-trial?v=1

# Documentation

Each type of sprite in the game has an object, so there is one for the player, boomerangs, walls, enemies, boosts and the goal.
Each object has the property 'pos' which is a list containing its x and y co-ordinates.
Most objects then have the property 'vel' which is how much the x and y co-ordinates change.
Some also have the property 'state' that determines if they are dead or alive etc.
All objects have the method 'update' which handles collisions and drawing the sprite on the screen
Some also have 'move' or 'move1' which handle moving the object to its new position, this is called inside update.
There are more specified methods for individual objects which I will cover when I write up the full documentation

