from tkinter import *
import RPi.GPIO as GPIO
import time
import random
#Color List
colorList = ["Red", "Yellow", "Blue", "Black", "Grey", "Brown", "White", "Green", "Purple", "Orange", "Light Blue", "Dark Blue", "Pink", "Dark Green",
             "Light Green"]
#Geth the colors
backgroundColor = colorList[random.randint(0, len(colorList)-1)]
lineColor = colorList[random.randint(0, len(colorList)-1)]
#Error Evoider
backgroundChange = False
lineChange = False
backgroundCounter = 0
lineCounter = 0
#Fullscreen
"""
height = 950
width = 1250
"""
#Get Some inputs
print("Welcome, please enter some basic information")
topSpeedLimit = int(input("Enter the top speed of the line: "))
bottomSpeedLimit = int(input("Enter the lowest speed of the line: "))
height = int(input("Enter canvas height: "))
width = int(input("Enter canvas width: "))
backgroundChangeBool = input("Do you want backgroundChange: ")
lineChangeBool  = input("Do you want lineChange: ")
#Act on some of those inputs
if (backgroundChangeBool == 'Yes' or backgroundChangeBool == 'yes'):
    backgroundChange = True
    backgroundRate = int(input("How often do you want the background to change(1 being the most): "))
    if (backgroundRate <= 0):
        backgroundRate = 1
    else:
        backgroundRate = backgroundRate
else:
    backgroundChange = False
if (lineChangeBool == "Yes" or lineChangeBool == 'yes'):
    lineChange = True
    lineRate = int(input("How often do you want the background to change(1 being the most): "))
    if (lineRate <= 0):
        lineRate = 1
    else:
        lineRate = lineRate
else:
    lineChange = False
#Do some dependant variabling
#Start Position
a=random.randint(0, width)
b=random.randint(0, height)
c=random.randint(0, width)
d=random.randint(0, height)
#Starting Speeds
speed=random.randint(1, 10)
speed1=random.randint(1, 10)
speed2=random.randint(1, 10)
speed3=random.randint(1, 10)
#Setup Window
window=Tk()
window.title("Satisfy")
#Setup canvas
canvas=Canvas(bg=backgroundColor, height=height, width=width, highlightthickness=0)
canvas.pack()
#Create line
bounceLine = canvas.create_line(a, b, c, d, fill=lineColor, width=5)
#Do the loop that runs the whole thing
def repeat():
    global a, b, c, d
    global bounceLine
    global speed, speed1, speed2, speed3
    global backgroundCounter, lineCounter
    a=a+speed
    b=b+speed1
    c=c+speed2
    d=d+speed3
    if (a>=width):
        speed=-random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (a<=0):
        speed=random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (b>=height):
        speed1=-random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (b<=0):
        speed1=random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (c>=width):
        speed2=-random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (c<=0):
        speed2=random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (d>=height):
        speed3=-random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1
    elif (d<=0):
        speed3=random.randint(bottomSpeedLimit, topSpeedLimit)
        backgroundCounter=backgroundCounter+1
        lineCounter=lineCounter+1

    if (backgroundChange and backgroundCounter >= backgroundRate):
        backgroundColor = colorList[random.randint(0, len(colorList)-1)]
        canvas.config(bg=backgroundColor)
        backgroundCounter = 0
    if (lineChange and lineCounter >= lineRate):
        lineColor = colorList[random.randint(0, len(colorList)-1)]
        canvas.itemconfig(bounceLine, fill=lineColor)
        lineCounter = 0

    canvas.coords(bounceLine, a, b, c, d)
    window.after(40, repeat)
repeat()
