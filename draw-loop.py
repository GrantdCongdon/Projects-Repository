from tkinter import *
import grid
#import time
import random
#line
g=200
g1=300
r=200
r1=300
#rectangle
a=300
a1=400
n=300
n1=400
u=50
#counter
s=2
i=2
c=2
ai=2
ia=2
rt=2
#rectangle
s=350
l=100
s1=450
l1=280
#oval
o=200
p=50
o1=300
p1=250
#circle
e=100
e1=100
e2=200
e3=200
#triangle
u1=50
limit=170
f=400
f1=500
move_1=False
blue="black"
tx=160
ty=260
tx1=140
ty1=310
tx2=90
ty2=320
tx3=140
ty3=330
tx4=90
ty4=380
tx5=160
ty5=340
tx6=230
ty6=380
tx7=180
ty7=330
tx8=230
ty8=320
tx9=180
ty9=310
#great more variables
smove=200
sgo=200
smove2=400
sgo2=400
speed1=random.randint(1,5)
speed2=random.randint(1,5)
function_text={'line': 'Function Complied ', 'square': 'Function Complied ',
               'clear': 'Function Complied', 'move line left':
               'Function Complied Draw Another Line ',
               'portable line':'Function Complied ', 'circle':
               'Function Complied ',
               'rectangle': 'Function Complied ', 'oval':'Function Complied ',
               'triangle': 'Function Complied ', 'move line right':
               'Function Complied Draw Another Line ',
               'move line up': 'Function Complied Draw Another Line ',
               'move line down':'Function Complied Draw Another Line ',
               'move square right': 'Function Complied Draw Another Square ',
               'move square left':'Function Complied Draw Another Square ',
               'move square up':'Funcion Complied Draw Another Square ',
               'move square down':'Function Complied Draw Another Square ',
               'move rectangle right':'Function Complied Draw Another Rectangle ',
               'move rectangle left':'Function Complied Draw Another Rectangle ',
               'move rectangle up':'Function Complied Draw Another Rectangle ',
               'move rectangle down':'Function Complied Draw Another Rectangle ',
               'move oval right':'Function Complied Draw Another Oval ',
               'move oval left':'Function Complied Draw Another Oval ',
               'move oval up':'Function Complied Draw Another Oval ',
               'move oval down':'Function Complied Draw Another Oval ',
               'move circle right':'Function Complied Draw Another Circle ',
               'move circle left':'Function Complied Draw Another Circle ',
               'move circle up':'Function Complied Draw Another Circle ',
               'move circle down':'Function Complied Draw Another Circle ',
               'move triangle':'Function Complied Draw Another Triangle ',
               'star':'Function Complied ', 'trapezoid':'Function Complied ',
               'exit':'Done!'}
window=Tk()
window.title("Draw Loop")
canvas = Canvas(bg="black", height=500, width=500, highlightthickness=0)
canvas.pack()
"""x=canvas.create_line(g, r, g1, r1, fill=blue)
grid.Grid(c=canvas, color="white", color1="blue", limit=500, limit1=500)
letsgo=canvas.create_rectangle(smove, sgo/2, smove*2, sgo, width=1, fill="dark blue")
160 260"""
def random_move():
    global letsgo
    global smove
    global sgo
    global smove2
    global sgo2
    global speed1
    global speed2
    smove=smove+speed1
    sgo=sgo+speed2
    smove2=smove2+speed1
    sgo2=sgo2+speed2
    if (smove2>=500):
        speed1=-5
    if (smove<=0):
        speed1=5
    if (sgo2>=500):
        speed2=-5
    if (sgo<=0):
        speed2=5
    canvas.coords(letsgo, smove, sgo2, smove2, sgo)
    window.after(25, random_move)
    
    
    
def line(event):
    global j
    global s
    if (s<3):
        j=canvas.create_line(g, r, g1, r1, fill="blue")
    #canvas.delete(j)
    j=canvas.create_line(g, r, g1, r1, fill="blue")
    s=4
def square(event):
    global y
    global i
    if (i<3):
        y=canvas.create_rectangle(a, n, a1, n1, fill="green")
    canvas.delete(y)
    y=canvas.create_rectangle(a, n, a1, n1, fill="green")
    i=4
def rectangle(event):
    global c
    global z
    if (c<3):
        z=canvas.create_rectangle(s, l, s1, l1, fill="gray")
    canvas.delete(z)
    z=canvas.create_rectangle(s, l, s1, l1, fill="gray")
    c=4
def oval(event):
    global ia
    global q
    if (ia<3):
        q=canvas.create_oval(o, p, o1, p1, fill="purple")
    canvas.delete(q)
    q=canvas.create_oval(o, p, o1, p1, fill="purple")
    ia=4
def circle(event):
    global ai
    global te
    if (ai<3):
        te=canvas.create_oval(e, e1, e2, e3, fill="red")
    canvas.delete(te)
    te=canvas.create_oval(e, e1, e2, e3, fill="red")
    ai=4
def triangle(event):
    global u
    global rt
    global zx
    global limit
    if (rt<3):
        zx=canvas.create_line(u1, f, u, f1, fill="pink")
    canvas.delete(zx)
    while(u<=limit):
        zx=canvas.create_line(u1, f, u, f1, fill="pink")
        u=u+1
    
    
    rt=4
def star(event):
    canvas.create_line(tx, ty, tx1, ty1, fill="blue", width=3)
    canvas.create_line(tx1, ty1, tx2, ty2, fill="blue", width=3)
    canvas.create_line(tx2, ty2, tx3, ty3, fill="blue", width=3)
    canvas.create_line(tx3, ty3, tx4, ty4, fill="blue", width=3)
    canvas.create_line(tx4, ty4, tx5, ty5, fill="blue", width=3)
    canvas.create_line(tx5, ty5, tx6, ty6, fill="blue", width=3)
    canvas.create_line(tx6, ty6, tx7, ty7, fill="blue", width=3)
    canvas.create_line(tx7, ty7, tx8, ty8, fill="blue", width=3)
    canvas.create_line(tx8, ty8, tx9, ty9, fill="blue", width=3)
    canvas.create_line(tx9, ty9, tx, ty, fill="blue", width=3)
def trap(event):
    m=300
    m1=260
    m2=400
    canvas.create_line(300, 100, 400, 100, fill="green")
    canvas.create_line(m, 100, m1, 140, fill="green")
    canvas.create_line(400, 100, 440, 140, fill="green")
    canvas.create_line(260, 140, 440, 140, fill="green")
    while (m<=400):
        canvas.create_line(m, 100, m1, 140, fill="green")
        m=m+1
    while (m1<=400):
        canvas.create_line(m, 100, m1, 140, fill="green")
        m1=m1+1
    while (m2<=440):
        canvas.create_line(400, 100, m2, 140, fill="green")
        m2=m2+1
def clear(event):
    canvas.delete(ALL)
    #grid.Grid(c=canvas, color="white", color1="blue", limit=500, limit1=500)
def move_triR():
    global u
    global u1
    global limit
    u=u+100
    u1=u1+100
    limit=limit+100
def move_circleR():
    global e
    global e2
    e=e+100
    e2=e2+100
def move_circleL():
    global e
    global e2
    e=e-100
    e2=e2-100
def move_circleU():
    global e1
    global e3
    e1=e1-100
    e3=e3-100
def move_circleD():
    global e1
    global e3
    e1=e1+100
    e3=e3+100
def move_ovalR():
    global o
    global o1
    o=o+100
    o1=o1+100
def move_ovalL():
    global o
    global o1
    o=o-100
    o1=o1-100
def move_ovalU():
    global p
    global p1
    p=p-100
    p1=p1-100
def move_ovalD():
    global p
    global p1
    p=p+100
    p1=p1+100
def move_rectR():
    global s
    global s1
    s=s+100
    s1=s1+100
def move_rectL():
    global s
    global s1
    s=s-100
    s1=s1-100
def move_rectU():
    global l
    global l1
    l=l-100
    l1=l1-100
def move_rectD():
    global l
    global l1
    l=l+100
    l1=l1+100
def move_sqR():
    global a
    global a1
    a=a+100
    a1=a1+100
def move_sqL():
    global a
    global a1
    a=a-100
    a1=a1-100
def move_sqU():
    global n
    global n1
    n=n-100
    n1=n1-100

def move_sqD():
    global n
    global n1
    n=n+100
    n1=n1+100
def move_line():
    #global x
    global g
    global g1
    global r
    global r1
    #global a
    #global a1
    #global n
    #global n1
    
    g=g-100
    g1=g1-100
    #canvas.coords(x, g, r, g1, r1)
def move_line1():
    global g
    global g1
    g=g+100
    g1=g1+100
def move_line2():
    global r
    global r1
    r=r+100
    r1=r1+100
def move_line3():
    global r
    global r1
    r=r-100
    r1=r1-100
def portable_line(event):
    canvas.create_line(100, 300, 200, 400, fill="orange")
def end():
    exit()
function= {'line':line, 'square':square, 'clear':clear, 'move line left':move_line,
           'portable line':portable_line, 'circle':circle, 'rectangle':rectangle,
           'oval':oval, 'triangle':triangle, 'move line right':move_line1,
           'move line up':move_line3, 'move line down':move_line2,
           'move square up':move_sqU, 'move square down':move_sqD,
           'move square right':move_sqR,'move square left':move_sqL,
           'move rectangle right':move_rectR, 'move rectangle left':move_rectL,
           'move rectangle down':move_rectD, 'move rectangle up':move_rectU,
           'move oval right':move_ovalR,'move oval left':move_ovalL,
           'move oval up':move_ovalU,'move oval down':move_ovalD,
           'move circle right':move_circleR,'move circle left':move_circleL,
           'move circle up':move_circleU,'move circle down':move_circleD,
           'move triangle':move_triR,'star':star, 'trapezoid':trap,'exit':end}
#canvas.create_line(100, 100, 300, 300, fill="blue")
canvas.grid()
intake = Entry(window, width=80, bg="light green")
spit = Text(window, width=60, height=4, wrap=WORD, background="dark green")
spit.grid(row=2, column=0, columnspan=2, sticky=N)
intake.grid(row=1, column=0, sticky=N)
global enter
def smart(event):
    enter = intake.get()
    global x
    global y
    try:
        put = function_text[enter]
        #function[enter]
        if (function[enter]==line):
            line(0)
        elif (function[enter]==square):
            square(0)
        elif (function[enter]==clear):
            clear(0)
        elif (function[enter]==circle):
            circle(0)
        elif (function[enter]==rectangle):
            rectangle(0)
        elif (function[enter]==oval):
            oval(0)
        elif (function[enter]==triangle):
            triangle(0)
        elif (function[enter]==move_line):
            #canvas.delete(x)
            #canvas.delete(x, g, r, g1, r1)
            move_line()
        elif (function[enter]==move_line2):
            move_line2()
        elif (function[enter]==move_line3):
            move_line3()
        elif (function[enter]==move_line1):
            move_line1()
        elif (function[enter]==move_sqR):
            move_sqR()
        elif (function[enter]==move_sqL):
            move_sqL()
        elif (function[enter]==move_sqU):
            move_sqU()
        elif (function[enter]==move_sqD):
            move_sqD()
        elif (function[enter]==move_rectR):
            move_rectR()
        elif (function[enter]==move_rectL):
            move_rectL()
        elif (function[enter]==move_rectD):
            move_rectD()
        elif (function[enter]==move_rectU):
            move_rectU()
        elif (function[enter]==move_ovalR):
            move_ovalR()
        elif (function[enter]==move_ovalL):
            move_ovalL()
        elif (function[enter]==move_ovalU):
            move_ovalU()
        elif (function[enter]==move_ovalD):
            move_ovalD()
        elif (function[enter]==move_circleR):
            move_circleR()
        elif (function[enter]==move_circleL):
            move_circleL()
        elif (function[enter]==trap):
                trap(0)
        elif (function[enter]==move_circleU):
            move_circleU()
        elif (function[enter]==move_circleD):
            move_circleD()
        elif (function[enter]==move_triR):
            move_triR()
        elif (function[enter]==star):
            star(0)
        elif (function[enter]==end):
            end()
        #put=" Function not yet available"
    except:
        put=" Function not yet available"
    spit.insert(END, put)
    intake.delete(0, END)
window.bind("<Return>", smart)
#random_move()
