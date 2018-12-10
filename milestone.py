#GlowScript 2.7 VPython
#URL: http://www.glowscript.org/#/user/jetsai/folder/MyPrograms/program/poolstarter.py
scene.bind('keydown', keydown_fun)     # Function for key presses
scene.bind('click', click_fun)         # Function for mouse clicks
scene.background = 0.8*vector(1, 1, 1) # Light gray (0.8 out of 1.0)
scene.width = 640                      # Make the 3D canvas larger
scene.height = 480


# +++ start of OBJECT_CREATION section
# These functions create "container" objects, called "compounds"

def make_cueball(starting_position = vector(15,0,0), starting_vel = vector(0,0,0)):
    """Makes a cue ball with a starting velocity of (0,0,0) at the right end of the map"""
    cueball = sphere(size = 1.0*vector(1,1,1), pos = starting_position)
    cueball.vel = starting_vel
    return cueball

def make_flag(starting_position = vector(0,0,0), starting_vel = vector(0,0,0)):
    """Makes a flag with a velocity of (0,0,0) in the center of the map"""
    hole = sphere(pos=vector(0,-.8,0), size=vec(1,1.5,1), color = vector(1, .7, .2))
    pole = box(size = vector(.2, 10, .2), pos = vector(0,0,0), color = vector(1,1,1))
    flag = triangle(
          v0=vertex( pos=vec(0,4,0), color = color.red ),
          v1=vertex( pos=vec(1.4,4.5,-1.5), color = color.blue ),
          v2=vertex( pos=vec(0,5,0), color = color.green))
    flag_objects = [hole, pole, flag]
    com_flag = compound(flag_objects, pos = starting_position)
    return com_flag
    
def make_blackHole(starting_position, starting_vel = vector(0,0,0)):
    """Makes a new moving blackHole with a starting position and default velocity with vector(0,0,0)"""
    blackHole = helix(size = 1.0*vector(1, 1, 1), pos = starting_position, color = color.black)   # ball is an object of class helix
    blackHole.vel = starting_vel          # This is the initial velocity
    return blackHole

# The ground is represented by a box (vpython's rectangular solid)
# http://www.glowscript.org/docs/GlowScriptDocs/box.html
ground = box(size = vector(40, 1, 20), pos = vector(0, -1, 0), color = vector(0, 1, 0))

# Creating the boundaries of the map (rectangular)
wallA = box(pos = vector(0, 0, -10), axis = vector(1, 0, 0), size = vector(40, 1, .2), color = vector(1.0, 0.7, 0.3)) # amber
wallB = box(pos = vector(-20, 0, 0), axis = vector(0, 0, 1), size = vector(20, 1, .2), color = vector(1.0, 0.7, 0.3))   # amber
wallC = box(pos = vector(0, 0, 10), axis = vector(1, 0, 0), size = vector(40, 1, .2), color = vector(1.0, 0.7, 0.3))    # amber
wallD = box(pos = vector(20, 0, 0), axis = vector(0, 0, 1), size = vector(20, 1, .2), color = vector(1.0, 0.7, 0.3))  # amber

# Creates a red tint for the scenery
DL = distant_light( direction=vec(0,20,0), 
                    color=color.red )
                    
# A stick that we will be able to control


# Making cueball
cueball = make_cueball()

# Making flag
flag = make_flag()

# Making a black hole
blackHole = make_blackHole(starting_position = vector(-9, 0, 0), starting_vel = vector(5,0,5))

# Making water
water = box(pos=vec(-15,0,5),  axis=vec(1,0,1),  size=vec(5,.2,7), color = color.cyan, opacity=.5)

# +++ end of OBJECT_CREATION section


# +++ start of ANIMATION section

# Other constants
RATE = 30                # The number of times the while loop runs each second
dt = 1.0/(1.0*RATE)      # The time step each time through the while loop
scene.autoscale = False  # Avoids changing the view automatically
scene.forward = vector(0, -3, -2)  # Ask for a bird's-eye view of the scene...

# This is the "event loop" or "animation loop"
# Each pass through the loop will animate one step in time, dt
#
while True:

    rate(RATE)   # maximum number of times per second the while loop runs

    # +++ Start of PHYSICS UPDATES -- update all positions here, every time step

    cueball.pos = cueball.pos + cueball.vel*dt #update cueball position
    blackHole.pos = blackHole.pos + blackHole.vel*dt #update blackHole position


    # +++ End of PHYSICS UPDATES -- be sure new objects are updated appropriately!


    # +++ Start of COLLISIONS -- check for collisions & do the "right" thing

    corral_collide(cueball)
    corral_collide(blackHole)

    # If the ball collides with the flagpole, give the cueball a vertical velocity
    if mag(cueball.pos - flag.pos) < 1.0:
        print("To infinity and beyond!")
        cueball.vel = vector(0, 1, 0)
    # If the ball collides with the blackHole, reset the ball to (0,0,0) and moves the blackHole to a random position
    if mag(cueball.pos - blackHole.pos) < 1.0:
        print("Oh no! The ball got sucked in!")
        cueball.pos = vector(15,0,0)
        blackHole.pos = vector(choice([-19,19]), 0.0, choice([-9,9]))    
    # If the ball collides with the water, rest the ball to (0,0,0)
    if mag(cueball.pos - water.pos) < 1.0:
        print("Oh no! You lost the ball in the water!")
        cueball.pos = vector(15,0,0)
    # +++ End of COLLISIONS



# +++ start of EVENT_HANDLING section -- separate functions for
#                                keypresses and mouse clicks...

def keydown_fun(event):
    """This function is called each time a key is pressed."""
    cueball.color = randcolor()
    key = event.key
    ri = randint(0, 10)
    print("key:", key, ri)  # Prints the key pressed -- caps only...

    amt = 0.42              # "Strength" of the keypress's velocity changes
    if key == 'up' or key in 'wWiI':
        cueball.vel = cueball.vel + vector(0, 0, -amt)
    elif key == 'left' or key in 'aAjJ':
        cueball.vel = cueball.vel + vector(-amt, 0, 0)
    elif key == 'down' or key in 'sSkK':
        cueball.vel = cueball.vel + vector(0, 0, amt)
    elif key == 'right' or key in "dDlL":
        cueball.vel = cueball.vel + vector(amt, 0, 0)
    elif key in ' rR':
        cueball.vel = vector(0, 0, 0) # Reset! via the spacebar, " "
        cueball.pos = vector(0, 0, 0)

def click_fun(event):
    """This function is called each time the mouse is clicked."""
    print("event is", event.event, event.which)

# +++ End of EVENT_HANDLING section



# +++ Other functions can go here...

def choice(L):
    """Implements Python's choice using the random() function."""
    LEN = len(L)              # Get the length
    randomindex = int(LEN*random())  # Get a random index
    return L[randomindex]     # Return that element

def randint(low, hi):
    """Implements Python's randint using the random() function.
       returns an int from low to hi _inclusive_ (so, it's not 100% Pythonic)
    """
    if hi < low:
        low, hi = hi, low               # Swap if out of order!
    LEN = int(hi) - int(low) + 1.       # Get the span and add 1
    randvalue = LEN*random() + int(low) # Get a random value
    return int(randvalue)               # Return the integer part of it

def randcolor():
    """Returns a vector of (r, g, b) random from 0.0 to 1.0."""
    r = random(0.0, 1.0)
    g = random(0.0, 1.0)
    b = random(0.0, 1.0)
    return vector(r, g, b)       # A color is a three-element vector
    
def corral_collide(ball):
    """Corral collisions!
       Ball must have a .vel field and a .pos field.
    """

     # If the ball hits wallA
    if ball.pos.z < wallA.pos.z:  # Hit -- check for z
        ball.pos.z = wallA.pos.z  # Bring back into bounds
        ball.vel.z *= -1.0        # Reverse the z velocity

    # If the ball hits wallB
    if ball.pos.x < wallB.pos.x:  # Hit -- check for x
        ball.pos.x = wallB.pos.x  # Bring back into bounds
        ball.vel.x *= -1.0        # Reverse the x velocity
    
    # If the ball hits wallC
    if ball.pos.z > wallC.pos.z: # Hit -- check for x
        ball.pos.z = wallC.pos.z # Bring back into bounds
        ball.vel.z *= -1.0       # Reverse the x velocity
    
    # If the ball hits wallD
    if ball.pos.x > wallD.pos.x: #Hit -- check for z
        ball.pos.x = wallD.pos.x # Bring back into bounds
        ball.vel.x *= -1.0        #Reverse the z velocity