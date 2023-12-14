import turtle
import winsound 
import math
import random
#import serial
from threading import Thread
from time import sleep

wn = turtle.Screen()
wn.bgcolor("gray")
wn.title("Gaza War")
wn.bgpic("back.gif")

turtle.register_shape("tank.gif")
turtle.register_shape("solider.gif")

border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("red")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(5)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

score = 0

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("red")
score_pen.penup()
score_pen.setposition(-20, 275)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Times New Roman", 15, "normal"))
score_pen.hideturtle()

player = turtle.Turtle()
player.shape("solider.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15

number_of_enemies = 8
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape("tank.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y =  random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 5

bullet = turtle.Turtle()
bullet.color("red")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(1,1)
bullet.hideturtle()

bulletspeed = 40

bulletstate = "ready"



    
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280: x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280: x = 280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        winsound.PlaySound("explosion-e+b", winsound.SND_ASYNC)
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

def isCollision_enemy_bullet(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 30: return True
    else: return False

def isCollision_enemy_player(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 25: return True
    else: return False

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# ser = serial.Serial('com3', 9600)
# global txt = ''
# def read_serial():
#     global txt
#     while True: txt = ser.readline()

# def control(txt):
#     if chr(txt[0]) == '0': fire_bullet()
#     elif chr(txt[0]) == '#': move_left()
#     elif chr(txt[0]) == '*': move_right()

# var = Thread(target=read_serial)
# var.daemon = True
# var.start()

# Main game loop
Game_Over = False
missed_enemies = 0
while True:
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        if enemy.xcor() > 270:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and Game_Over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 2: Game_Over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            enemyspeed *= -1

        if enemy.xcor() < -270:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and Game_Over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 2:
                        Game_Over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            enemyspeed *= -1

        if isCollision_enemy_bullet(bullet, enemy):
            winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC) 
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            enemyspeed += 0.5

            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
        if isCollision_enemy_player(player, enemy):
            winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC) 
            Game_Over = True
        if Game_Over == True:
            player.hideturtle()
            bullet.hideturtle()
            for e in enemies:
                e.hideturtle()
            wn.bgpic("Game_Over.png")
            break

    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"