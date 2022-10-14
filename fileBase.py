import mysql.connector
import upload
from tkinter import *
import os
import picamera
camera = picamera.PiCamera()
export = upload.Upload()
dwnld = upload.Download()
h = 100
w = 200
screenWidth = 100
screenHeight = 20
r=0
c=0
counter=0
dbc = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="filebase"
)
m = dbc.cursor()
w = Tk()
users = []
w.title("Login")
def createFrame(row, column, columnspan, stick):
    display = Frame(w)
    display.grid(row=row, column=column, columnspan=columnspan, sticky=stick)
    return display
def loginPage(display):
    username = Entry(display, width=screenWidth, background="white")
    username.grid(row=0, column=1, sticky=N)

    password = Entry(display, width=screenWidth, background="grey", show="*")
    password.grid(row=1, column=1, stick=S)

    usernameText = Label(display, width=10, height=1, text="Username: ")
    usernameText.grid(row=0, column=0, sticky=W)

    passwordText = Label(display, width=10, height=1, text="Password: ")
    passwordText.grid(row=1, column=0, sticky=W)
    return username, password

def createButtons(y, buttons, messageWigdet=None, width=12, stick=S):
    global r, c
    r=0
    c=0
    for b in buttons:
        def cmd(x=b):
            click(x, messageWigdet, y)
        Button(y, text=b, width=width, command=cmd).grid(row=r, column=c,
                                                     sticky=stick)
        c=c+1
        if (c>5):
            c=0
            r=r+1
def createInterface(y, r, c, stick):
    interface = Text(y, width=screenWidth, height=2, bg="Black", fg="White")
    interface.grid(row=r, column=c, sticky=stick)
    return interface
def output(y, message):
    y.delete(END)
    y.insert(END, message)
def takePicture(image, y):
    output(y, "3")
    sleep(1)
    output(y, "2")
    sleep(1)
    output(y, "1")
    sleep(1)
    output(y, "Now!")
    camera.capture(image)
login = ["Login"]
options = ["Record", "Recall", "Exit"]
documents = ["Birth Certificate", "Marriage Liscense", "Liscense", "Passport",
          "Go Back"]
def click(key, y, x):
    global newInterface, documentButtons, mode
    if (key==login[0]):
        logn()
    elif (key==options[0]):
        y.destroy()
        newInterface = createFrame(0, 0, 2, N)
        messageInterface = createInterface(newInterface, 0, 0, N)
        documentButtons = createFrame(1, 0, 1, W)
        documentOptions = createButtons(documentButtons, documents)
        mode = 0
    elif (key==options[1]):
        y.destroy()
        newInterface = createFrame(0, 0, 2, N)
        messageInterface = createInterface(newInterface, 0, 0, N)
        documentButtons = createFrame(1, 0, 1, W)
        documentOptions = createButtons(documentButtons, documents)
        mode = 1
    elif (key==options[2]):
        w.destroy()
    elif (key==documents[0] and mode==0):
        name = credentials[1]+"-birthCertificate.png"
        folder = credentials[0]+credentials[1]
        takePicture(name)
        upload.CreateFolder('', '',
                            '', 'Grant', folder)
        export.picture('', '',
                            '', 'Grant/'+folder,
                       '/home/pi/python/database/'+name, name)
        os.remove(name)
        output(y, "Documented")
    elif (key==documents[1] and mode==0):
        name = credentials[1]+"-marriageLiscense.png"
        folder = credentials[0]+credentials[1]
        takePicture(name)
        upload.CreateFolder('', '',
                            '', 'Grant', folder)
        export.picture('', '',
                            '', 'Grant/'+folder,
                       '/home/pi/python/database/'+name, name)
        os.remove(name)
        output(y, "Documented")
    elif (key==documents[2] and mode==0):
        name = credentials[1]+"-liscense.png"
        folder = credentials[0]+credentials[1]
        takePicture(name)
        upload.CreateFolder('', '',
                            '', 'Grant', folder)
        export.picture('', '',
                            '', 'Grant/'+folder,
                       '/home/pi/python/database/'+name, name)
        os.remove(name)
        output(y, "Documented")
    elif (key==documents[3] and mode==0):
        name = credentials[1]+"-passport.png"
        folder = credentials[0]+credentials[1]
        takePicture(name)
        upload.CreateFolder('', '',
                            '', 'Grant', folder)
        export.picture('', '',
                            '', 'Grant/'+folder,
                       '/home/pi/python/database/'+name, name)
        os.remove(name)
        output(y, "Documented")
    elif (key==documents[0] and mode==1):
        name = credentials[1]+"-birthCertificate.png"
        folder = credentials[0]+credentials[1]
        dwnld.picture('', '', '',
                      'Grant/'+folder, name, '/home/pi/python/database/'+name)
        
    elif (key==documents[4]):
        newInterface.destroy()
        documentButtons.destroy()
        messageBoard = createFrame(0, 0, 2, N)
        interfaceButtons = createFrame(1, 0, 2, W)
        interface = createInterface(messageBoard, 0, 0, N)
        createButtons(interfaceButtons, options, interface)
    else:
        print("Error")
def logn():
    u = credentials[0].get()
    p = credentials[1].get()
    m.execute("SELECT id, username FROM users")
    result = m.fetchall()
    for x in result:
        if (p==str(x[0]) and u==x[1]):
            lgn.destroy()
            btns.destroy()
            messageBoard = createFrame(0, 0, 2, N)
            interfaceButtons = createFrame(1, 0, 2, W)
            interface = createInterface(messageBoard, 0, 0, N)
            createButtons(interfaceButtons, options, interface)
lgn = createFrame(0, 0, 2, N)
credentials = loginPage(lgn)
btns = createFrame(1, 0, 1, W)
createButtons(btns, login)
w.mainloop()
