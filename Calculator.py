from tkinter import *
import random
# speed of sound 320, speed of light 300000000, us sun 149597887.5, pi 3.141592654
def factorial(n):
    try:
        n=int(n)
    except:
        return "--> Error!"
    if n == 0:
        return 1
    if n > 40:
        return "--> Answer will not fit on screen!"
    if n < 0:
        return "--> Error!"
    
    ans=n
    while n>1:
        ans=ans*(n-1)
        n=n - 1
        return ans
def to_roman(n):
    try:
        n = int(n)
    except:
        return "--> Error"
    if n > 4999:
        return "out of range"
    numberBreaks = (1000,900,500,400,100,90,50,40,10,9,5,4,1)
    letters = {1000 : "M", 900 : "CM", 500 : "D", 400 : "CD", 100 : "C",
               90 : "XC", 50 : "L", 40 : "XL", 10 : "X", 9 : "IX", 5 : "V",
               4 : "IV", 1 : "I" }
    result = ""
    for value in numberBreaks:
        while n >= value:
            result = result+letters[value]
            n = n-value
    return result

def to_binary(n):
    try:
        n = int(n)
        return bin(n)[2:]
    except:
        return "--> Error!"
    
    return "-> binary"
def from_binary(n):
    try:
        return int(n, 2)
    except:
        return "--> Error!"
    
    return "binary -> 10"

chioce = random.randint(0, 10), random.randint(0, 9001)

def click(key):
    if key == "=":
        try:
            result = str(eval(display.get()))[0:10]
            display.insert(END, " = " + result)
        except:
            display.insert(END, " --> Error!")
    elif key == constants_list[0]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "3.141592654")
    elif key == constants_list[1]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "300000000 m/s")
    elif key == constants_list[2]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "320 m/s")
    elif key == constants_list[3]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "149597887.5")
    elif key == "C":
        display.delete(0, END)
    elif key == function_list[0]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, factorial(n))
    elif key == function_list[1]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, to_roman(n))
    elif key == function_list[2]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, to_binary(n))
    elif key == function_list[3]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, from_binary(n))
    elif key == ulimate_button_list[0]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "Google one one one and 100 zeros")
    elif key == ulimate_button_list[1]:
        n = display.get()
        display.delete(0, END)
        display.insert(END, "Google Plex one one with google zeros")
    elif key == ulimate_button_list[2]:
        n = display.get()
        display.delete(0, END)
# the grant constant explains how many times an atom's election(s) will spin around it at some point.
        display.insert(END, "16.505050")
    elif key == ulimate_button_list[3]:
        n = display.get()
        display.delete(0, END)  
        display.insert(END, chioce)
    else:
        display.insert(END, key)

window = Tk()
window.title("MyCalculator")

top_row = Frame(window)
top_row.grid(row=0, column=0, columnspan=2, sticky=N)

display = Entry(top_row, width=45, bg="light green")
display.grid()

num_pad = Frame(window)
num_pad.grid(row=1, column=0, sticky=W)

ulimate_button = Frame(window)
ulimate_button.grid(row=4, column=0, sticky=S)

operator = Frame(window)
operator.grid(row=1, column=1, sticky=E)

constants = Frame(window)
constants.grid(row=3, column=0, sticky=W)

functions = Frame(window)
functions.grid(row=3, column=1, stick=E)

function_list = [
    'factorial (!)',
    '-> roman', # I don't travel the world you know
    '-> binary', # I don't go tour traveling
    'binary -> 10' ] # whatg does the 10 do with anything
constants_list = [
    'pi',
    'speed of light (m/s)',
    'speed of sound (m/s)',
    'ave dist to sun (km)' ]

operator_list = [
    '*', '/',
    '+', '-',
    '(', ')',
    'C' ]

num_pad_list = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3',
    '0', '.', '=' ]

r = 0 # row counter
c = 0 # column counter
ulimate_button_list = [
    'super button',
    'mega button',
    'the Grant constant',
    'random number']

for b in ulimate_button_list:
    def cmd(x=b):
        click(x)
    Button(ulimate_button, text=b, width=45, command=cmd).grid(row=r, column=c)
    r = r+1

for b in function_list:
    def cmd(x=b):
        click(x)
    Button(functions, text=b, width=13, command=cmd).grid(row=r, column=c)
    r = r+1

for btn_text in constants_list:
    def cmd(x=btn_text):
        click(x)
    Button(constants, text=btn_text, width=22, command=cmd).grid(row=r, column=c)
    r = r+1

for btn_text in num_pad_list:
    def cmd(x=btn_text):
        click(x)
    Button(num_pad, text=btn_text, width=5, command=cmd).grid(row=r, column=c)
    c = c+1
    if c > 2:
        c = 0
        r = r+1

for b in operator_list:
    def cmd(x=b):
        click(x)
    Button(operator, text=b, width=5, command=cmd).grid(row=r, column=c)
    c = c+1
    if c > 1:
        c = 0
        r = r+1

window.mainloop()

