Creat tutoral before start game where you teach player how to play

game class:
controler for entire game
handle scenes and gameplay

tutorial class:
handle everthing related to playing the tutorial

level class:
create and draw levels.

animation run at 8 frames per second


a little bit of an offset between the background


run: play when pressed (hold)
idle robot: plays when player does nothing and is in robot mode
shoot: key press. can shoot when run
jump: key press. can shoot when jump and can jump when running
transform: key press. cannot shoot or do anything else when animation plays.
driving: can shoot maybe secondary weapon. can't shoot blaster? cannot jump
idle car: plays when player does nothing and is in car modes
blasterGet: plays on key press when first press shoot?
useItem: key press (like shooting but different button)

hold down z to grab blaster and have to hold z to keep blaster out. When z is let go, put away blaster.
use cipher from coding challenges as writing on walls of game maybe hmmm


## TO DO LIST
## HEADER
**BOLD**
* LIST
*I*

make enemies shoot player :0
enemy sprites have blasters


try speed and angle to move bullet


Finish checkcollsion function in game

enemy blaster needs to show 1 thing, finish rotate cords methord in blaster class

compare time.time to stoptime make sure the values are within the proper range.

Make MORE level stucture tile sprites (including middle tile piece)


FIX AllframesImg!!!!
Look for unneeded code!!!!!!!

Offset might be hint about vetical glitch thingy. Collisions are working better. fixed ground collision and reduced lag.✓

ADD RUNNING ✓
allow transforming while running ✓
Change background color of anim, see which frame the issue is on.✓
**NOTE TO SELF**: Scaling issue is caused by pygame transform scale method (fixed-ish when using smoothscale but fuzzy)✓

add new blaster in game :)

after resetstates is run the animations don't change (look at the order of which things are happening or something else)

