http://www.glowscript.org/#/user/jetsai/folder/MyPrograms/program/poolstarter.py #click to view/run program 

GlowScript 2.7 VPython
scene.bind('keydown', keydown_fun)     # Function for key presses
scene.bind('click', click_fun)         # Function for mouse clicks
scene.background = vector(0.38, 0, .642) #(0.8 out of 1.0)
scene.width = 600                    # Make the 3D canvas larger
scene.height = 480

# Game constants
totalPoints = 0 # Start out with 0 points

# Object creation section
def make_cuestick(ball):
    cuewidth = 10
    cuestick = box(pos = vec(ball.pos.x + cuewidth / 2 + 1.5, ball.pos.y, ball.pos.z), size = vec(cuewidth, .35, .35), texture = 'https://i.imgur.com/U0Zwa1U.jpg')
    cuestick.moveAngle = 0
    cuestick.usedShots = 0
    return cuestick

def make_cueball(starting_position = vector(15,0,0), starting_vel = vector(0,0,0)):
    """Makes a cue ball with a starting velocity of (0,0,0) at the right end of the map"""
    cueball = sphere(size = 1.0*vector(1,1,1), pos = starting_position)
    cueball.vel = starting_vel
    cueball.cueBallsLeft = 10 # Start out with 10 balls
    return cueball

def make_flag(starting_position = vector(-18,0,0), starting_vel = vector(0,0,0)):
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

# Making power slider 
scene.caption = "Press the spacebar to hit the cueball with the stick! (Stick only appears when all balls are not moving)\nVary the power that you hit the cueball with: \n\n"
def setspeed(s):
    wt.text = '{:1.2f}'.format(s.value)
sl = slider(min=0, max=60, value=60, length=300, bind=setspeed, right=100)
wt = wtext(text='{:1.2f}'.format(sl.value))
scene.append_to_caption(' Power Level\n')

# Creating ground and boundaries
ground = box(size = vector(40, 1, 20), pos = vector(0, -1, 0), texture = "https://i.imgur.com/KL8DYzs.jpg")
wallA = box(pos = vector(0, 0, -10), axis = vector(1, 0, 0), size = vector(40, 1, .2), texture = "https://i.imgur.com/lJSuUIr.jpg") 
wallB = box(pos = vector(-20, 0, 0), axis = vector(0, 0, 1), size = vector(20, 1, .2), texture = "https://i.imgur.com/lJSuUIr.jpg")  
wallC = box(pos = vector(0, 0, 10), axis = vector(1, 0, 0), size = vector(40, 1, .2), texture = "https://i.imgur.com/lJSuUIr.jpg")    
wallD = box(pos = vector(20, 0, 0), axis = vector(0, 0, 1), size = vector(20, 1, .2), texture = "https://i.imgur.com/lJSuUIr.jpg")  

# Making cueball and other balls
cueball = make_cueball()
testball = sphere(pos = vector(0,0,0), size = vector(1,1,1), color = color.red)
testball.vel = vector(0,0,0)
testball2 = sphere(pos = vector(-2,0,2), size = vector(1,1,1), color = color.red)
testball2.vel = vector(0,0,0)
testball3 = sphere(pos = vector(-2,0,-2), size =vector(1,1,1), color = color.red)
testball3.vel = vector(0,0,0)
testball4 = sphere(pos = vector(-2,0,0), size = vector(1,1,1), color = color.red)
testball4.vel = vector(0,0,0)
testball5 = sphere(pos = vector(-4,0,0), size = vector(1,1,1), color = color.red)
testball5.vel = vector(0,0,0)
testball6 = sphere(pos = vector(-4,0,2), size = vector(1,1,1), color = color.red)
testball6.vel = vector(0,0,0)
testball7 = sphere(pos = vector(-4,0,-2), size = vector(1,1,1), color = color.red)
testball7.vel = vector(0,0,0)
testball8 = sphere(pos = vector(-4,0,4), size = vector(1,1,1), color = color.red)
testball8.vel = vector(0,0,0)
testball9 = sphere(pos = vector(-4,0,-4), size = vector(1,1,1), color = color.red)
testball9.vel = vector(0,0,0)

# List of balls
sphereList = [cueball, testball, testball2, testball3, testball4, testball5, testball6, testball7, testball8, testball9]

# Making cuestick
cuestick = make_cuestick(cueball)
isMoving = False

# Making flag
flag = make_flag()

# Making a black hole
blackHole = make_blackHole(starting_position = vector(-9, 0, 0), starting_vel = vector(5,0,5))

# Making water hazard
water = box(pos=vec(-12,0,0),  axis=vec(1,0,0),  size=vec(5,.5,6), texture = "https://i.imgur.com/7c23FjJ.jpg", opacity=.5)

# Make red rings
smoke = []
Nrings = 20
x0, y0, z0 = -18.5,0,.5
r0 = 0.5
spacing = 2
thick = r0/3
dr = 0.005
dthick = thick/Nrings
gray = 1
for i in range(Nrings):
  smoke.append(ring(pos=vector(x0,y0+spacing*i,z0), axis=vector(0,1,0),
                radius=r0+dr*i, thickness=thick-dthick*i, color= vector(.964, .732, .894)))
y = 0
dy = spacing/20
top = Nrings-1

# +++ end of OBJECT_CREATION section

# +++ start of ANIMATION section
# Other constants
RATE = 30                # The number of times the while loop runs each second
dt = 1.0/(1.0*RATE)      # The time step each time through the while loop
scene.autoscale = False  # Avoids changing the view automatically
#scene.camera.pos = vector(0,4,55)
scene.forward = vector(0, -.2, -.2)  # Ask for a bird's-eye view of the scene...

while True:

    rate(RATE)   # maximum number of times per second the while loop runs
    
    # +++ Start of PHYSICS UPDATES -- update all positions here, every time step
    cueball.pos = cueball.pos + cueball.vel*dt # update cueball position
    cueball.vel = cueball.vel * 0.98  #friction
    if mag(cueball.vel) < .3: # stop the ball if under a certain velocity
        cueball.vel = vec(0,0,0)
        
    blackHole.pos = blackHole.pos + blackHole.vel*dt #update blackHole position
    
    testball.pos = testball.pos + testball.vel*dt #update testball positions
    testball.vel = testball.vel * .95
    if mag(testball.vel)<.2:
        testball.vel = vec(0,0,0)
    testball2.pos = testball2.pos + testball2.vel*dt
    testball2.vel = testball2.vel * .95
    if mag(testball2.vel)<.2:
        testball2.vel = vec(0,0,0)
    testball3.pos = testball3.pos + testball3.vel*dt
    testball3.vel = testball3.vel * .95
    if mag(testball3.vel)<.2:
        testball3.vel = vec(0,0,0)
    testball4.pos = testball4.pos + testball4.vel*dt
    testball4.vel = testball4.vel * .95
    if mag(testball4.vel)<.2:
        testball4.vel = vec(0, 0, 0)
    testball5.pos = testball5.pos + testball5.vel*dt
    testball5.vel = testball5.vel * .95
    if mag(testball5.vel)<.2:
        testball5.vel = vec(0, 0, 0)
    testball6.pos = testball6.pos + testball6.vel*dt
    testball6.vel = testball6.vel * .95
    if mag(testball6.vel)<.2:
        testball6.vel = vec(0, 0, 0)
    testball7.pos = testball7.pos + testball7.vel*dt
    testball7.vel = testball7.vel * .95
    if mag(testball7.vel)<.2:
        testball7.vel = vec(0, 0, 0)
    testball8.pos = testball8.pos + testball8.vel*dt
    testball8.vel = testball8.vel * .95
    if mag(testball8.vel)<.2:
        testball8.vel = vec(0, 0, 0)
    testball9.pos = testball9.pos + testball9.vel*dt
    testball9.vel = testball9.vel * .95
    if mag(testball9.vel)<.2:
        testball9.vel = vec(0, 0, 0)
    
    # +++ End of PHYSICS UPDATES 

        # Move the smoke rings
    for i in range(Nrings):
        # Raise the smoke rings
        smoke[i].pos = smoke[i].pos+vector(0,dy,0)
        smoke[i].radius = smoke[i].radius+(dr/spacing)*dy
        smoke[i].thickness = smoke[i].thickness - (dthick/spacing)*dy
    y = y+dy
    if y >= spacing:
        # Move top ring to the bottom
        y = 0
        smoke[top].pos = vector(x0, y0, z0)
        smoke[top].radius = r0
        smoke[top].thickness = thick
        top = top-1
    if top < 0:
        top = Nrings-1
    
    # +++ Start of COLLISIONS -- check for collisions & do the "right" thing

    #ensures cueball, blackHole, and other balls stay within the board
    corral_collide(cueball) 
    corral_collide(blackHole)
    corral_collide(testball)
    corral_collide(testball2)
    corral_collide(testball3)
    corral_collide(testball4)
    corral_collide(testball5)
    corral_collide(testball6)
    corral_collide(testball7)
    corral_collide(testball8)
    corral_collide(testball9)
    # If the cueball collides with the flagpole, you win!
    if mag(cueball.pos - flag.pos) < 1.0:
        print("Good job! You won!")
        cueball.vel = vector(0, 0, 0)
        cueball.pos = vector(-20,10,0)
        winObject1 = box(pos = vector(0,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/RVIN1TA.png")
        winObject2 = box(pos = vector(6,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/z5j59UZ.jpg")
        winObject3 = box(pos = vector(-6,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/H6A53.jpg")
        winText = text(text='OMG! YOU WON! YOU HAD ' + totalPoints + ' POINT(S)!', pos=vec(-11.5,10,5),
          color=color.cyan, billboard=True, emissive=True)

    # If you run out of cueballs, you lose!
    if cueball.cueBallsLeft < 1:
        cueball.visible = False
        cuestick.visible = False
        print("Oh no! You ran out of cueballs!")
        
        loseObject1 = box(pos = vector(0,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/zrCDsSG.png")
        loseObject2 = box(pos = vector(6,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/z5j59UZ.jpg")
        loseObject3 = box(pos = vector(-6,5,5), size = vector(5,5,5), texture = "https://i.imgur.com/H6A53.jpg")
        loseText = text(text='YOU HAD ' + totalPoints + ' POINT(S), BUT YOU RAN OUT OF CUEBALLS!', pos=vec(-11.5,10,5),
          color=color.red, billboard=True, emissive=True)
          
    # If the other balls collide with the flagpole, points are added
    if mag(testball.pos - flag.pos) < 1.0:
        testball.pos = vec(0, -5, 0)
        testball.visible = False
        print("Point added!")
        totalPoints += 1
        
    if mag(testball2.pos - flag.pos) < 1.0:
        testball2.pos = vec(0, -5, 0)
        testball2.visible = False
        print("Point added!")
        totalPoints += 1
        
    if mag(testball3.pos - flag.pos) < 1.0:
        testball3.pos = vec(0, -5, 0)
        testball3.visible = False
        print("Point added!")
        totalPoints += 1
        
    if mag(testball4.pos - flag.pos) < 1.0:
        testball4.pos = vec(0, -5, 0)
        testball4.visible = False
        print("Point added!")
        totalPoints += 1
    
    if mag(testball5.pos - flag.pos) < 1.0:
        testball5.pos = vec(0, -5, 0)
        testball5.visible = False
        print("Point added!")
        totalPoints += 1
        
    if mag(testball6.pos - flag.pos) < 1.0:
        testball6.pos = vec(0, -5, 0)
        testball6.visible = False
        print("Point added!")
        totalPoints += 1
    
    if mag(testball7.pos - flag.pos) < 1.0:
        testball7.pos = vec(0, -5, 0)
        testball7.visible = False
        print("Point added!")
        totalPoints += 1
    
    if mag(testball8.pos - flag.pos) < 1.0:
        testball8.pos = vec(0, -5, 0)
        testball8.visible = False
        print("Point added!")
        totalPoints += 1
    
    if mag(testball9.pos - flag.pos) < 1.0:
        testball9.pos = vec(0, -5, 0)
        testball9.visible = False
        print("Point added!")
        totalPoints += 1
        
    # If the ball collides with the blackHole, reset the ball to (0,0,0) and moves the blackHole to a random position
    if mag(cueball.pos - blackHole.pos) < 1.0:
        print("Oh no! The ball got sucked in!")
        cueball.pos = vector(15,0,0)
        blackHole.pos = vector(choice([-19,19]), 0.0, choice([-9,9]))
        cuestick.pos = vec(cueball.pos.x + cuestick.size.x/2 + 1.5, cueball.pos.y, cueball.pos.z)
        cuestick.axis = vec(10, 0, 0)
        cueball.cueBallsLeft-=1
        
    # If the ball collides with the water, reset the ball to (0,0,0)
    if cueball.pos.x > -14.5 and cueball.pos.x < -10.5 and cueball.pos.z > -3 and cueball.pos.z < 3:
        print("Oh no! You lost the ball in the water!")
        cueball.pos = vector(15,0,0)
        cueball.vel = vector(0,0,0)
        cueball.cueBallsLeft-=1
        
    # collision checking and response: ideal, elastic collisions
    for i in range(len(sphereList)):
        for j in range(i + 1, len(sphereList)):
            if collide(sphereList[i], sphereList[j]) == True:
                # diff = the vector between the two
                diff = sphereList[i].pos - sphereList[j].pos
                dtan = rotate(diff, radians(90), vector(0, 1, 0))

                # get the two velocities
                vi = sphereList[i].vel
                vj = sphereList[j].vel
                # undo the last time step
                sphereList[i].pos -= sphereList[i].vel * dt * 1.1
                sphereList[j].pos -= sphereList[j].vel * dt * 1.1
                # find the radial and tangent parts
                vi_rad = proj(vi, diff)
                vi_tan = proj(vi, dtan)
                vj_rad = proj(vj, -diff)
                vj_tan = proj(vj, dtan)
                # swap the radials and keep the tangents
                sphereList[i].vel =  vj_rad + vi_tan
                sphereList[j].vel =  vi_rad + vj_tan
    # +++ End of COLLISIONS
    
    # Cuestick Handling
    if (cueball.vel.x != 0 or cueball.vel.z != 0) and isMoving == False:
        isMoving = True
        cuestick.visible = False
        
    if (cueball.vel.x == 0 and cueball.vel.z == 0) and isMoving == True and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel) == 0 and mag(testball6.vel)== 0 and mag(testball7.vel)== 0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        isMoving = False
        cuestick.pos = vec(cueball.pos.x + cuestick.size.x/2 + 1.5, cueball.pos.y, cueball.pos.z)
        cuestick.axis = vec(10, 0, 0)
        cuestick.visible = True
    
# +++ start of EVENT_HANDLING section -- separate functions for
#                                keypresses and mouse clicks...

def keydown_fun(event):
    """This function is called each time a key is pressed. Using arrows or WASD, you rotate the stick. """
    key = event.key
    if (key == 'up' or key in 'wWiI') and isMoving == False and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel) == 0 and mag(testball6.vel)== 0 and mag(testball7.vel)== 0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        cuestick.rotate(angle = pi/100, axis = vec(0, 1, 0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle += pi/100
    elif (key == 'down' or key in 'sSkK') and isMoving == False and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel)==0 and mag(testball6.vel)==0 and mag(testball7.vel)==0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        cuestick.rotate(angle = -pi/100, axis = vec(0, 1, 0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle += -pi/100
    elif (key == 'left' or key in 'aAjJ') and isMoving == False and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel)==0 and mag(testball6.vel)==0 and mag(testball7.vel)==0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        cuestick.rotate(angle = pi/100, axis = vec(0, 1, 0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle += pi/100
    elif (key == 'right' or key in "dDlL") and isMoving == False and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel)==0 and mag(testball6.vel)==0 and mag(testball7.vel)==0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        cuestick.rotate(angle = -pi/100, axis = vec(0, 1, 0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle += -pi/100
    elif key in 'rR':
        cueball.vel = vector(0, 0, 0) 
        cueball.pos = vector(15, 0, 0)
        cuestick.rotate(angle = -cuestick.moveAngle, axis = vec(0,1,0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle = 0    
        cueball.cueBallsLeft-=1
        
    #Hitting the cueball at the angle of the cuestick
    elif key in ' ' and isMoving == False and mag(testball.vel) == 0 and mag(testball2.vel)==0 and mag(testball3.vel)==0 and mag(testball4.vel)==0 and mag(testball5.vel)==0 and mag(testball6.vel)==0 and mag(testball7.vel)==0 and mag(testball8.vel)==0 and mag(testball9.vel)==0:
        xvel = cuestick.axis.x/(abs(cuestick.axis.x)+abs(cuestick.axis.z))
        zvel = cuestick.axis.z/(abs(cuestick.axis.x)+abs(cuestick.axis.z))
        cueball.vel = vector(-sl.value*xvel,0,-sl.value*zvel)
        cuestick.rotate(angle = -cuestick.moveAngle, axis = vec(0,1,0), origin = vec(cueball.pos.x, cueball.pos.y, cueball.pos.z))
        cuestick.moveAngle = 0
        cuestick.usedShots +=1
    elif key in 'xX':
        cueball.pos = vector(-18,0,0)
    print("You have " + cueball.cueBallsLeft + " balls left!" )
    print("You have a total of " + totalPoints + " points!")

def click_fun(event):
    """This function is called each time the mouse is clicked."""
    print("event is", event.event, event.which)

# +++ End of EVENT_HANDLING section



# +++ Other functions

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

def collide(a, b):
    diff = a.pos - b.pos
    if mag(diff) < a.radius + b.radius + .1:
        return True
    else:
        return False

def corral_collide(ball):
    """Corral collisions!
       Ball must have a .vel field and a .pos field.
    """

     # If the ball hits wallA
    if ball.pos.z < wallA.pos.z+1:  # Hit -- check for z
        ball.pos.z = wallA.pos.z+1  # Bring back into bounds
        ball.vel.z *= -1.0        # Reverse the z velocity

    # If the ball hits wallB
    if ball.pos.x < wallB.pos.x+1:  # Hit -- check for x
        ball.pos.x = wallB.pos.x+1  # Bring back into bounds
        ball.vel.x *= -1.0        # Reverse the x velocity
    
    # If the ball hits wallC
    if ball.pos.z > wallC.pos.z-1: # Hit -- check for x
        ball.pos.z = wallC.pos.z-1 # Bring back into bounds
        ball.vel.z *= -1.0       # Reverse the x velocity
    
    # If the ball hits wallD
    if ball.pos.x > wallD.pos.x-1: #Hit -- check for z
        ball.pos.x = wallD.pos.x-1 # Bring back into bounds
        ball.vel.x *= -1.0        #Reverse the z velocity