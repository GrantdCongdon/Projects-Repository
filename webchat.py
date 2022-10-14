from datetime import datetime
from ftplib import FTP_TLS
from time import sleep
from subprocess import call
import time
import subprocess
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import upload
export = upload.Upload()
imprt = upload.Download()
loopLap=0
picture_list = []
audio_list = []
video_list = []
print('Welcome to IotChat 3.1.4 Open Alpha')
try:
    password = input("Enter Password: ") #Make sure you belong on the chat
    if password == '42':
        print('yay')
        name = input('What is your name: ') #Identify Themselves
        name = str(name) #Make sure name enters is a string
        pic = 1
        camera = picamera.PiCamera() #Define the camera
        camera.resolution = (680, 480) #adjust camera resolution
        camera.rotation = 180 #rotate camera so that it is rightside up
        while True: # infine loop so user can notify multiple people
                note = input('Do you want to inform others you are on the webchat: ') #Gets the input of wether you want to email a person to tell if they are on the webchat
                if (note == 'yes' or note == 'Yes'): #If statement that checks if the user said yes
                    msg = MIMEMultipart()
                    fromad = input("What is your email: ") # takes input of user email
                    epass = input("Enter email password: ") # takes input of user password
                    who = input('Who do be want to send notification to (Enter Email): ') #Gets the input of the reciever of the email
                    fromaddr = fromad #defines variable of who the email is from
                    toaddr = who #defines variable of who the email is to
                    msg['From'] = fromaddr #set who the email is from
                    msg['To'] = toaddr #set who the email is to
                    msg['Subject'] = "Webchat" #set subject
                    body = (name + ' is on the web chat server') #Create the text in the body
                    msg.attach(MIMEText(body, 'plain')) #attach the body to the email
                    p = MIMEBase('application', 'octet-stream')
                    msg.attach(p)
                    s = smtplib.SMTP('smtp.gmail.com', 587) #set up and create object for email function
                    s.starttls() #start email function
                    s.login(fromaddr, epass) # login with the users email
                    text = msg.as_string() #set up email
                    s.sendmail(fromaddr, toaddr, text) #send and create email
                    s.quit() #Quit email function
                    print ('Message sent') #tells the user that the email was sent
                else: # if user says no the send notification question then the following code executes
                    break #breaks the infinte loop
        while True: #Loop for send muliple pictures, audio recordings, and video is one run of the program
            while True:
                text = input('Do you want to upload a message: ')
                if (text == 'yes' or text == 'Yes' or text == "yse" or text == 'sey' or text == 'eys' or text == 'sye'):
                    text_input = str(input("Do you want to send: \n"))
                    """with open("message.txt", "w") as f:
                        f.write(text_input)"""
                    imprt.files('', '', '', '/Webchat',
                                    'index.html', 'index.html')
                    if (loopLap==0):
                        with open("index.html", "w+") as h: #overrights the old index page and adds the first link to the picture the user sent up
                            h.write('<!doctype html><!--2-->\n')
                            h.write('<html><!--2-->\n<head><!--2-->\n')
                            h.write('<meta charset="UTF-8"><!--2-->\n')
                            h.write('<title>IOT Chat</title><!--2-->\n')
                            h.write('<style>\nbody {text-align: center;}\n')
                            h.write('body {background-color: rgb(200, 100, 50)}<!--2-->\n')
                            h.write('</style><!--2-->\n')
                            h.write('</head><!--2-->\n')
                            h.write('<body><!--2-->\n')
                            h.write('<h1>Welcome to the IOT chat!</h1><!--2-->\n')
                            h.write('<h2>Below are almost live files to see and hear</h2><!--2-->\n')
                            h.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                            #h.write('<a href="'+wer+'">'+wer+'</a>\n')
                            h.write('<h4>'+text_input+'</h4><!--2-->\n')
                            h.write('<!--1--><!--2-->\n') #makerplace for next edite
                            h.write('</body><!--2-->\n</html><!--2-->\n')
                        loopLap=loopLap+1
                    else:
                        r = open("index.html", 'r') #opens index page in reading mode
                        rd = r.read() #reads the index page and stores all the lines into a variabl
                        rd = rd.split("<!--2-->")
                        r.close() #closes the index page
                        f = open("index.html", "w") #opens the index page again this time in writing
                        for line in rd: #Loop that looks for the maker and if it finds it then adds a few lines of code to the index page include the new picture link
                            if (line=="<!--1-->"): #checks of rmaker
                                f.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                                #f.write('<a href="'+wer+'">'+wer+'</a>\n')
                                f.write('<h4>'+text_input+'</h5><!--2-->\n')
                                f.write('<!--1--><!--2-->\n')
                            else: #if the line does not include the maker then the section of the program simply rights what would be there anyways
                                f.write(line+'<!--2-->\n')
                        f.close()
                    export.files('', '', #uploads the index page back to the internet for another download and edit
                                '', '/Webchat',
                                '/home/pi/python/index.html', 'index.html')
                else:
                    break
            while True: #Loop for if users want to send multiple pictures
                pho = input('Do you want to take a Picture: ') #asks if user wants to send a picture
                if (pho == 'yes' or pho == 'Yes' or pho == "yse" or pho == 'sey' or pho == 'eys' or pho == 'sye'): #checks if the user inputed anything close to yes
                    wer = input('What do you want to call the picture: ') #Asks user for the name of their picture
                    time_name = time.strftime("%D_%T")
                    time_name = time_name+".jpg"
                    camera.capture('/home/pi/python/'+time_name) #takes the picture
                    picture_list.append(time_name)
 
                    export.picture('', '', #uploads the picture to the internet by home made class by Grant Congdon
                                   '', '/Webchat',
                                   '/home/pi/python/'+wer, wer, permission=False)
                    imprt.files('', '', #imports the index page of the website for editing
                                '', '/Webchat',
                                   'index.html', 'index.html')
                    if (loopLap==0): #if this is the first time running through the program
                        with open("index.html", "w") as h: #overrights the old index page and adds the first link to the picture the user sent up
                            h.write('<!doctype html><!--2-->\n')
                            h.write('<html><!--2-->\n<head><!--2-->\n')
                            h.write('<meta charset="UTF-8"><!--2-->\n')
                            h.write('<title>IOT Chat</title><!--2-->\n')
                            h.write('<style>\nbody {text-align: center;}\n')
                            h.write('body {background-color: rgb(200, 100, 50)}<!--2-->\n')
                            h.write('</style><!--2-->\n')
                            h.write('</head><!--2-->\n')
                            h.write('<body><!--2-->\n')
                            h.write('<h1>Welcome to the IOT chat!</h1><!--2-->\n')
                            h.write('<h2>Below are almost live files to see and hear</h2><!--2-->\n')
                            h.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                            h.write('<a href="'+time_name+'" target="_blank">'+wer+'</a><!--2-->\n')
                            h.write('<!--1--><!--2-->\n') #makerplace for next edite
                            h.write('</body><!--2-->\n</html><!--2-->\n')
                        loopLap=loopLap+1 #adds one to loopLap so that the program knows that it is the second time running through the loop
                    else: #if it is the second time or more running through the loop
                        #r = open("index.html", 'r') #opens index page in reading mode
                        #read = r.readlines() #reads the index page and stores all the lines into a variable
                        #r.close() #closes the index page
                        #f = open("index.html", "w") #opens the index page again this time in writing mode

                        r = open("index.html", 'r') #opens index page in reading mode
                        rd = r.read() #reads the index page and stores all the lines into a variabl
                        rd = rd.split("<!--2-->")
                        r.close() #closes the index page
                        f = open("index.html", "w")
                        
                        for line in rd: #Loop that looks for the maker and if it finds it then adds a few lines of code to the index page include the new picture link
                            if (line=="<!--1-->"): #checks of marker
                                f.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                                f.write('<a href="'+wer+'">'+wer+'</a><!--2-->\n')
                                f.write('<!--1--><!--2-->\n')
                            else: #if the line does not include the maker then the section of the program simply rights what would be there anyways
                                f.write(line+'<!--2-->\n')
                        f.close() # closes the index page in writing mode
                    export.files('', '', #uploads the index page back to the internet for another download and edit
                                    '', '/Webchat',
                                    '/home/pi/python/index.html', 'index.html')
                else: # else breaks the infinte loop and continues on the next section of code
                    break # breaks while loop
            while True: #Loop so that users can take multiple recordings
                audio = input('Do you want take a audio recording: ') #ask user if they want to take an audio recording
                if (audio == 'yes' or audio == 'Yes'): #check if user said yes
                    wer = input("What do you want to call the audio recording: ")
                    timee = int(input('How long do you want to record: ')) # Takes the user input of how long to record
                    #now = datetime.now() #sets a variable that contains current date and time
                    #now = str(now) #convert variable to a string
                    #now =now[0:10] + '_' + now[11:13] + '_' + now[14:16] + '_' + now[17:19] #extract time from the variable
                    time_name = time.strftime("%D_%T")
                    record = "arecord --device=hw:1 --format S16_LE --rate 44100 --duration=" + timee + " -c1 " + time_name + ".wav" #set a variable that will be executed in command line
                    #timee = int(timee)
                    sleep( timee ) #rest for the value of time
                    
                    convert = "lame -b 16 " + name + '_' + time_name + ".wav " + time_name + ".mp3" #convert the file to a .mp3 file
                    delete = "rm " + time_name + ".wav" #set another variable command that will be executed in terminal
                    delete2 = "rm " + time_name + ".mp3" #another vaiable that will be executed in termainal
                    print("Recording Started")
                    call([record], shell=True) #execute command record
                    print('Done Recording')  #tell the user that they are done recording
                    call([convert], shell=True) #execute command convert
                    sleep(6) #rest for 6 seconds
                    call([delete], shell=True) #execute command delete

                    filename = '/home/pi/' + name + '_' + now + '.mp3' #set a filename for audio record upload
                    """
                    ftppath = '/webchat/'
                    s.cwd (ftppath)
                    f= open (filename, 'rb')
                    s.storbinary('STOR '+ name + '_' + now + '.mp3', f)
                    """
                    export.audio('', '', #upload the audio recording to the internet using external home made program
                                    '', '/Webchat',
                                    '/home/pi/python/'+time_name+".mp3", time_name+".mp3")
                    
                    time_name = time_name+".mp3"
                    audio_list.append(time_name)
                    
                    call([delete2], shell=True) #execute command delete2
                    imprt.files('', '', #import the index page from the website
                                    '', '/Webchat',
                                    'index.html', 'index.html')
                    if (loopLap==0): #checks if it is the first time running through the program
                        with open("index.html", "w") as h: #if so then writes over the previous index page and adds the link to the audio recording and creates a maker
                            h.write('<!doctype html><!--2-->\n')
                            h.write('<html><!--2-->\n<head><!--2-->\n')
                            h.write('<meta charset="UTF-8"><!--2-->\n')
                            h.write('<title>IOT Chat</title><!--2-->\n')
                            h.write('<style>\nbody {text-align: center;}\n')
                            h.write('body {background-color: rgb(200, 100, 50)}<!--2-->\n')
                            h.write('</style><!--2-->\n')
                            h.write('</head><!--2-->\n')
                            h.write('<body><!--2-->\n')
                            h.write('<h1>Welcome to the IOT chat!</h1><!--2-->\n')
                            h.write('<h2>Below are almost live files to see and hear</h2><!--2-->\n')
                            h.write('<h3>'+name+' : '+time.strftime("%D %T")+'</h3><!--2-->\n')
                            h.write('<a href="'+time_name+'">'+wer+'</a><!--2-->\n')
                            h.write('<!--1--><!--2-->\n') #the marker
                            h.write('</body><!--2-->\n</html><!--2-->\n')                            
                        loopLap=loopLap+1 #tells the computer that it is not the first time running through the program anymore
                    else: #runs if it is not the first time running through the program
                        r = open("index.html", 'r') # opens the index page in read mode
                        rd = r.read() # reads all the lines and stores it in a variable
                        rd = rd.split("<!--2-->")
                        r.close() # closes the file
                        f = open("index.html", "w") # opens the index file in writing mode
                        for line in read: # loop checks to see if it sees the marker if it is then adds a new link to the webpage and makes a new mark
                            if (line=="<!--1-->"):
                                f.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                                f.write('<a href="'+time_name+'">'+wer+'</a><!--2-->\n')
                                f.write('<!--1--><!--2-->\n')
                            else: # if the loop doesn't see the marker then it writes the line that would be in the program anyways
                                f.write(line+"<!--2-->\n")
                        f.close() #closes the file in write mode
                    export.files('', '', #uploads the index file make to the website so that it can be used by others
                                    '', '/Webchat',
                                    '/home/pi/python/index.html', 'index.html')
                else: # else the program will break the loop and continue to the next section of programing
                    break
            while True:
                    video = input('Do you want to take a video: ')
                    if video ==('yes'):
                        wer = input('What do you want to call the video recording: ')
                        wer = str(wer)
                        tim = input('Timespan of vdieo recording: ')
                        tim = int(tim)
                        
                        time_name = time.strftime("%D_%T")
                        
                        camera.start_recording(time_name + '.h264')
                        sleep( tim )
                        camera.stop_recording()
                        print('Video done') 
                        delete3 = time_name + '.h264'
                        delete4 = time_name + '.mp4'
                        convert = 'MP4Box -add ' + time_name + '.h264 ' + time_name + '.mp4'
                        call([convert], shell=True)
                        sleep(4.5)

                        filename = '/home/pi/' + w + '.mp4'
                        """
                        ftppath = '/webchat/'
                        s.cwd (ftppath)
                        f= open (filename, 'rb')
                        s.storbinary('STOR ' + w + '.mp4', f)"""
                        
                        export.video('', '',
                                    '', '/Webchat',
                                    '/home/pi/python/'+time_name+".mp4", time_name+".mp4")
                        
                        time_name = time_name + '.mp4'
                        video_list.append(time_name)
                        
                        call([delete3], shell=True)
                        call([delete4], shell=True)
                        imprt.files('', '',
                                    '', '/Webchat',
                                    'index.html', 'index.html')
                        if (loopLap==0):
                            with open("index.html", "w") as h:
                                h.write('<!doctype html><!--2-->\n')
                                h.write('<html><!--2-->\n<head><!--2-->\n')
                                h.write('<meta charset="UTF-8"><!--2-->\n')
                                h.write('<title>IOT Chat</title><!--2-->\n')
                                h.write('<style>\nbody {text-align: center;}\n')
                                h.write('body {background-color: rgb(200, 100, 50)}<!--2-->\n')
                                h.write('</style><!--2-->\n')
                                h.write('</head><!--2-->\n')
                                h.write('<body><!--2-->\n')
                                h.write('<h1>Welcome to the IOT chat!</h1><!--2-->\n')
                                h.write('<h2>Below are almost live files to see and hear</h2><!--2-->\n')
                                h.write('<h3>'+name+' : '+time.strftime("%D %T")+'</h3><!--2-->\n')
                                h.write('<a href="'+time_name+'">'+wer+'</a><!--2-->\n')
                                h.write('<!--1--><!--2-->\n')
                                h.write('</body><!--2-->\n</html><!--2-->\n')                            
                            loopLap=loopLap+1
                        else:
                            r = open("index.html", 'r')
                            rd = r.read()
                            rd = rd.split("<!--2-->")
                            r.close()
                            f = open("index.html", "w")
                            for line in read:
                                if (line=="<!--1-->"):
                                    f.write('<h3>'+name+':'+time.strftime("%D %T")+'</h3><!--2-->\n')
                                    f.write('<a href="'+time_name+'">'+wer+'</a><!--2-->\n')
                                    f.write('<!--1--><!--2-->\n')
                                else:
                                    f.write(line+"<!--2-->\n")
                            f.close()
                        export.files('', '',
                                    '', '/Webchat',
                                    '/home/pi/python/index.html', 'index.html')
                    else:
                        break
            ask_exit = input("Do you want to exit the Iot chat: ")
            if (ask_exit == "yes" or ask_exit == "Yes"):
                for value in picture_list:
                    upload.Delete('', '', '',
                           '/Webchat', value)
                for value in audio_list:
                    upload.Delete('', '', '',
                           '/Webchat', value)
                for value in video_list:
                    upload.Delete('', '', '',
                           '/Webchat', value)
                print("Webchat Exited")
                break
except KeyboardInterrupt:
    for value in picture_list:
        upload.Delete('', '', '',
                      '/Webchat', value)
    for value in audio_list:
        upload.Delete('', '', '',
                      '/Webchat', value)
    for value in video_list:
        upload.Delete('', '', '',
                      '/Webchat', value)
    print("\nWebchat Exited")
