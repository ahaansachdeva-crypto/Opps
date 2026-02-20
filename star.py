import turtle
import colorsys

t = turtle.Turtle()
t.speed(-1000)
turtle.bgcolor("black")

h = 0
t.width(2)

for i in range(200):
    color = colorsys.hsv_to_rgb(h, 1, 1)
    t.pencolor(color)
    t.forward(i * 0.7)
    t.left(777) # star angle
    h += 0.015

turtle.done()