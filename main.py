import turtle
import time
from bird import Bird

# constants
WIDTH, HEIGHT = 636, 764

# Frames per second
FPS = 60
frame_duration = 1.0 / FPS

# game variables
scroll = 0
scroll_speed = 4

# screen setup
wn = turtle.Screen()
wn.title("Flappy Bird")
wn.bgcolor("light blue")
wn.setup(WIDTH,HEIGHT)
wn.tracer(0)

# disable resizing
canvas = wn.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(False, False)

# pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

# register shapes
images = ["graphics/bg.gif",
          "graphics/bird1.gif",
          "graphics/bird2.gif",
          "graphics/bird3.gif",
          "graphics/ground.gif",
          "graphics/pipe.gif",
          "graphics/restart.gif"]
for image in images:
    wn.register_shape(image)

# bird
bird = Bird(-100, 0, "circle", "green")

while True:
    start_time = time.time()

    scroll -= scroll_speed
    if abs(scroll) > 35:
        scroll = 0

    # render background
    pen.shape("graphics/bg.gif")
    pen.goto(-450,20)
    pen.stamp()
    pen.goto(400,20)
    pen.stamp()
    pen.shape("graphics/ground.gif")
    pen.goto(scroll, -350)
    pen.stamp()

    # render bird
    bird.update()
    bird.render(pen)

    # update the screen
    wn.update()

    # clear the screen
    pen.clear()
    
    # calculate elapsed_time
    elapsed_time = time.time() - start_time
    time_to_sleep = frame_duration - elapsed_time

    # ensure the loop runs at correct speed
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)
