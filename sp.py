import turtle
import colorsys

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")

h = 0
t.width(2)

for i in range(300):    
    color = colorsys.hsv_to_rgb(h, 1, 1)
    t.pencolor(color)
    t.forward(i * 0.5)
    t.left(59)
    h += 0.005

turtle.done()
