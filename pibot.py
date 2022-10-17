import serial
import sys
from gpiozero import MCP3008
from Adafruit_IO import MQTTClient
from Adafruit_IO import Client
from time import sleep
import os
from sense_hat import SenseHat
from picamera import PiCamera
import upload
import time
import subprocess
from subprocess import call
import os
#from gps import *
from time import *
import time
import threading
from datetime import datetime
from time import sleep
import os
from gps import *
from time import *
import time
import threading
examplelat = str(41.480186)
examplelong = str(-81.143860)
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
def gps_location():
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      gpslatitude = (gpsd.fix.latitude)
      gpslongitude = (gpsd.fix.longitude)
      os.system('clear')
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."   
#set varaible
x=0
graph_list = []
picture_list = []
image_list = []
list_value = 0
x=1
y=1
i=0
l=0
tt=0
loopLap=0
loopLap2=0
loopLap3=0
export=upload.Upload()
imprt=upload.Download()
#setup
ADAFRUIT_IO_USERNAME = 'Yeloay'
ADAFRUIT_IO_KEY = '87324f6c2bf14a90ae1af3ff020a9cba'
FEED_ID = 'Pibot'
aio = Client('87324f6c2bf14a90ae1af3ff020a9cba')
s=SenseHat()
c=PiCamera()
c.resolution = (640, 480)
#start serial communication
serialMsg = serial.Serial("/dev/ttyACM0", 9600)
def active_index():
  with open('index.html', 'w+') as f:
    f.write('<!doctype html>\n')
    f.write('<html>\n<head>\n')
    f.write('<meta charset="UTF-8">\n')
    f.write('<title>Grant Homepage</title>\n')
    f.write('<style>\nbody {text-align: center;}\n')
    f.write('body {background-color: rgb(200, 100, 50)}\n')
    f.write('</style>\n')
    f.write('</head>\n<body>\n')
    f.write('<h1>Welcome to Pibot Homepage!</h1>\n')
    f.write('<h2>Pibot Active waiting for uploads...</h2>')
    f.write('</body>\n</html>')
  export.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                    'Grant', '/home/pi/pibot/pibot/index.html', 'index.html',
                    permission=True)
  return 0
def unactive_index():
  with open('index.html' 'w') as f:
    f.write('<!doctype html>\n')
    f.write('<html>\n<head>\n')
    f.write('<meta charset="UTF-8">\n')
    f.write('<title>Grant Homepage</title>\n')
    f.write('<style>\nbody {text-align: center;}\n')
    f.write('body {background-color: rgb(200, 100, 50)}\n')
    f.write('</style>\n')
    f.write('</head>\n<body>\n')
    f.write('<h1>Welcome to Pibot Homepage!</h1>\n')
    f.write('<h2>Pibot Unactive waiting for connection...</h2>')
    f.write('</body>\n</html>')
  export.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
               'Grant', '/home/pi/pibot/pibot/index.html', 'index.html',
               permission=True)
  return 0
#picture function
def picture2(path, timestamp=False):
  c.start_preview()
  if timestamp:
    tp = time.strftime("%D %T")
    c.annotate_text = tp
  c.capture(path)
  c.stop_preview()
def pressure():
  p = s.get_pressure()
  tp = time.strftime("%H:%M")
  p=p/100
  p = str(p)
  return tp, p
def read_sensor1():
  os.system("sudo modprobe w1-gpio")
  os.system("sudo modprobe w1-therm")
  time1 = time.strftime("%H:%M")
  os.chdir("/sys/bus/w1/devices/28-0000093bcf49")
  with open("w1_slave", "r") as file1:
      tempfile = file1.read()
  file1_line2 = tempfile.split("\n")[1]
  tempnumber = file1_line2.split(" ")[9]
  tempfirst = float(tempnumber[2:])
  tempfirst = tempfirst / 1000
  temp1 = float(tempfirst)
  t1 = str(temp1)
  os.chdir("/home/pi/upload")
  return time1, t1
def read_sensor2():
  os.system("sudo modprobe w1-gpio")
  os.system("sudo modprobe w1-therm")
  time2 = time.strftime("%H:%M")
  os.chdir("/sys/bus/w1/devices/28-0000093c5814")
  with open("w1_slave", "r") as file2:
      tempfile2 = file2.read()
  file2_line2 = tempfile2.split("\n")[1]
  tempnumber2 = file2_line2.split(" ")[9]
  tempfirst2 = float(tempnumber2[2:])
  tempfirst2 = tempfirst2 / 1000
  temp2=float(tempfirst2)
  t2 = str(temp2)
  os.chdir("/home/pi/upload")
  return time2, t2
def temp():
  a = read_sensor1()[1]
  b = read_sensor2()[1]
  temptime = time.strftime("%H:%M")
  a = float(a)
  b = float(b)
  avgtemp = (a+b)/2
  avgtemp=round(avgtemp)
  avgtemp = str(avgtemp)
  return temptime, avgtemp
def humidity():
  h = s.get_humidity()
  th = time.strftime("%H:%S")
  h = str(h)
  return th, h
def picture(path):
  c.start_preview()
  time.sleep(5)
  c.capture(path)
  c.stop_preview()
#connect to adafruit
def connect(client):
  client.subscribe(FEED_ID)
  active_index()
#disconnect function
def disconnect(client):
  c.close()
  unactive_index()
  sys.exit(0)
#Adafruit Communications go into message function
def message(client, feed_id, payload, retain):
  print("Starting")
  global x
  global temp
  global pressure
  global humidity
  global list_value
  global name_list
  global y
  global i
  global l
  global tt
  global temp_list
  global loopLap
  #Convert adafruit value which are in unicode to usable types
  feed_id = str(feed_id)
  payload = int(payload)
  if feed_id=="Pibot" and payload==5:
    serialMsg.write("r2000\n")
    serialMsg.write("l2000\n")
    sleep(1)
    serialMsg.write("r1500\n")
    serialMsg.write("l1500\n")
  elif feed_id=="Pibot" and payload==13:
    serialMsg.write("r1000\n")
    serialMsg.write("l1000\n")
    sleep(1)
    serialMsg.write("r1500\n")
    serialMsg.write("l1500\n")
  elif feed_id=="Pibot" and payload==10:
    serialMsg.write("r1000\n")
    serialMsg.write("l2000\n")
    sleep(0.45)
    serialMsg.write("r1500\n")
    serialMsg.write("l1500\n")
  elif feed_id=="Pibot" and payload==8:
    serialMsg.write("r2000\n")
    serialMsg.write("l1000\n")
    sleep(0.45)
    serialMsg.write("r1500\n")
    serialMsg.write("l1500\n")
  elif feed_id=="Pibot" and payload==0:
    serialMsg.write("a600\n")
  elif feed_id=="Pibot" and payload==2:
    serialMsg.write("a2400\n")
  elif feed_id=="Pibot" and payload==1:
    serialMsg.write("a1500\n")
  elif feed_id=="Pibot" and payload==6:
    unactive_index()
    client.on_disconnect = disconnect
    exit()
  elif feed_id=="Pibot" and payload==16:
    tempupload=temp()[1]
    tempupload=str(tempupload)
    aio.send('Data_Readings', "\n"+tempupload+"*C")
  elif feed_id=="Pibot" and payload==17:
    humidity=round(s.get_humidity())
    humidity=str(humidity)
    aio.send('Data_Readings', "\n"+humidity+"% humidity")
  elif feed_id=="Pibot" and payload==18:
    pressure=round(s.get_pressure())
    pressure=str(pressure)
    aio.send('Data_Readings', "\n"+pressure+" milibars")
  elif feed_id=="Pibot" and payload==20:
    d = time.strftime("%m-%d-%Y")
    ti1 = time.strftime("%H:%M:%S")
    datetime = d+"_"+ti1+".jpg"
    img=datetime
    picture_list.append(img)
    picture2('/home/pi/pibot/pibot/'+img, timestamp=True)
    export.picture('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                   'Grant', '/home/pi/pibot/pibot/'+picture_list[loopLap], picture_list[loopLap],  permission=False)
    
    imprt.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                'Grant', 'index.html', 'index.html')
    if (loopLap==0):
      with open("index.html", "w") as h:
        h.write('<!doctype html>\n')
        h.write('<html>\n<head>\n')
        h.write('<meta charset="UTF-8">\n')
        h.write('<title>Grant Homepage</title>\n')
        h.write('<style>\nbody {text-align: center;}\n')
        h.write('body {background-color: rgb(200, 100, 50)}\n')
        h.write('</style>\n')
        h.write('<style>\n')
        h.write("#map {\n")
        h.write("height: 400px;\n")
        h.write("width: 100%;\n")
        h.write("}\n")
        h.write("</style>\n")
        h.write("</head>\n")
        h.write("<body>\n")
        h.write("<h3>Map</h3>\n")
        h.write('<div id="map"></div>\n')
        h.write("<script>\n")
        h.write("function initMap() {\n")
        h.write("var uluru = {lat: "+examplelat+", lng: "+examplelong+"};\n")
        h.write("var map = new google.maps.Map\n(document.getElementById('map'), {zoom: 14, center: uluru});\n")
        h.write("var marker = new google.maps.Marker({position: uluru, map: map});\n}\n")
        h.write("</script>")
        h.write("</head>\n")
        h.write("<body>\n")
        h.write("<h1>Welcome to Grant's Homepage</h1>\n")
        h.write('<img src="'+picture_list[loopLap]+'" height="500" width="800">\n')
        h.write("<h2>Below is a link to Pibot Picture Location</h2>\n")
        h.write('<p> <a href="'+picture_list[loopLap]+'">'+picture_list[loopLap]+'</a></p>\n')
        h.write('<!--1-->\n')
        h.write('<!--2-->\n')
        h.write('<script async defer\n src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCDVWUnDjq7AtfOdXWfEX8cZSuSXs9T_y8&callback=initMap">\n</script>')
        h.write('</body>\n</html>')
      loopLap=loopLap+1
    else:
      with open('index.html', 'r') as r:
        read = r.readlines()
      f = open('index.html', 'w')
      for line in read:
        if (line=="<!--1-->\n"):
          f.write('<p><a href="'+picture_list[loopLap]+'">'+picture_list[loopLap]+'</a></p>\n')
          f.write('<!--1-->\n')
        elif (line=='<img src="'+picture_list[loopLap-1]+'" height="500" width="800">\n'):
          f.write('<img src="'+picture_list[loopLap]+'" height="500" width="800">\n')
        else:
          f.write(line)
      f.close()
      loopLap=loopLap+1
    export.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                 'Grant', '/home/pi/pibot/pibot/index.html', 'index.html',
                  permission=True)
    x=x+1
    os.system("rm *.html")
    os.system("rm *.jpg")
    print("Success")
  elif feed_id=="Pibot" and payload==21:
    imprt.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                'Grant', 'index.html', 'index.html')
    #l = gpstest()[1]
    #la = gpstest()[0]
    ti1 = time.strftime("%H:%M")
    t1 = temp()[1]
    p1 = pressure()[1]
    h1 = humidity()[1]
    at1 = time.strftime("%H:%M")
    time.sleep(60)
    t2 = temp()[1]
    p2 = pressure()[1]
    h2 = humidity()[1]
    at2 = time.strftime("%H:%M")
    time.sleep(60)
    t3 = temp()[1]
    p3 = pressure()[1]
    h3 = humidity()[1]
    at3 = time.strftime("%H:%M")
    time.sleep(60)
    t4 = temp()[1]
    p4 = pressure()[1]
    h4 = humidity()[1]
    at4 = time.strftime("%H:%M")
    time.sleep(60)
    t5 = temp()[1]
    p5 = pressure()[1]
    h5 = humidity()[1]
    at5 = time.strftime("%H:%M")
    ti2 = time.strftime("%H:%M")
    d = time.strftime("%m-%d-%Y")
    title = d+"_"+ti1+"-"+ti2
    datetime = d+"_"+ti1+"-"+ti2+".html"
    graph_list.append(datetime)
    it = temp()[1]
    ip = pressure()[1]
    ih = humidity()[1]
    it = float(it)
    ip = float(ip)
    ih = float(ih)
    it = round(it, 2)
    ip = round(ip, 2)
    ih = round(ih, 2)
    it = str(it)
    ip = str(ip)
    ih = str(ih)
    pot = MCP3008(0)
    interpot = (pot.value)
    interpot = str(round(interpot, 3))
    interpot = str(interpot)
    img_name = tim+'.jpg'
    image_list.append(img_name)
    picture('/home/pi/upload/'+image_list[loopLap]+'.jpg')
    with open(datetime, "w+") as t:
      t.write('<!doctype html>\n')
      t.write('<html>\n<head>\n')
      t.write('<meta charset="UTF-8">\n')
      t.write('<meta http-equiv="refresh" content="10" >\n')
      t.write('<style>body {background-color: rgb(10, 250, 10)}</style>')
      t.write('<title>HAT Weather Station</title>\n')
      t.write('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n')
      t.write('<script type="text/javascript">\n')
      t.write('google.charts.load("current", {"packages":["corechart"]});\n')
      t.write('google.charts.setOnLoadCallback(drawChart);\n')
      t.write('function drawChart() {\n')
      t.write('var data = google.visualization.arrayToDataTable([\n')
      t.write('["Time", "Temp*C", "Pressure (bars)", "Humidity(%)"],\n')
      t.write('[' + '"' + at1 + '"' + ', ')
      t.write(t1 + ', '+p1+', '+h1+'],\n')
      t.write('[' + '"' + at2 + '"' + ', ')
      t.write(t2 + ', '+p2+', '+h2+'],\n')
      t.write('[' + '"' + at3 + '"' + ', ')
      t.write(t3 + ', '+p3+', '+h3+'],\n')
      t.write('[' + '"' + at4 + '"' + ', ')
      t.write(t4 + ', '+p4+', '+h4+'],\n')
      t.write('[' + '"' + at5 + '"' + ', ')
      t.write(t5 + ', '+p5+', '+h5+'],\n')
      t.write(']);\n')
      t.write('var options = {\n')
      t.write('title: "Gear Weather Station for ' + d +'",\n')
      t.write('curveType: "function",\nlegend: { position: "bottom" }\n')
      t.write('};\n')
      t.write('var chart = new\n')
      t.write('google.visualization.LineChart(document.getElementById("curve_chart")\n')
      t.write(');\n')
      t.write('chart.draw(data, options);\n}\n')
      t.write('</script>\n')
      t.write('</head>\n')
      t.write('<body>\n')
      t.write('<center><div id="curve_chart" style="width: 900px; height: 500px">\n')
      t.write('</div></center>')
      t.write('<center><h3>Temperature is '+it+'*C | Pressure is '+ip+' bars | Humidity is '+ih+'%</h3></center>')
      t.write('<center><img src="'+image_list[loopLap2]+'" alt="Picture of House" height="500" width="800">')
      #t.write('<center><h3>The reading of the potentiometer is: ' + interpot + ' volts</h3></center>')
      #t.write('<center><p>The Location of the Robot is'+la, l+'</p><center>')
      t.write('</body>')
      t.write('</html>')
    if (loopLap2==0):
      with open("index.html", "w") as h:
        h.write('<!doctype html>\n')
        h.write('<html>\n<head>\n')
        h.write('<meta charset="UTF-8">\n')
        h.write('<title>Grant Homepage</title>\n')
        h.write('<style>\nbody {text-align: center;}\n')
        h.write('body {background-color: rgb(200, 100, 50)}\n')
        h.write('</style>\n')
        h.write('</head>\n')
        h.write('<body>')
        h.write("<h1>Welcome to Grant's Homepage</h1>\n")
        h.write('<h2>Below is a Link to a Weather Graph</h2>\n')
        h.write('<p><a href="'+graph_list[loopLap]+'">'+graph_list[loopLap]+'</a></p>\n')
        h.write('<!--1-->\n')
        h.write('<!--2-->\n')
        h.write('</body>\n</html>')
      loopLap2=loopLap2+1
    else:
      with open('index.html', 'r') as r:
        read = r.readlines()
      f = open('index.html', 'w')
      for line in read:
        if (line=='<!--2-->\n'):
          #f.write('<h2>Below are Links to Weather Graphs</h2>\n')
          for value in graph_list:
            f.write('<p><a href="'+graph_list[loopLap]+'">'+graph_list[loopLap]+'</a></p>\n')
            list_value=list_value+1
            f.write('<!--2-->\n')
            list_value=0
        else:
          f.write(line)
    graph = upload.Upload()
    graph.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                'Grant', '/home/pi/upload/'+datetime, datetime,
                permission=False)
    index = upload.Upload()
    index.files('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                'Grant', '/home/pi/upload/index.html', 'index.html',
                permission=True)
    """pic = upload.Upload()
    pic.picture('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
                'Grant', '/home/pi/upload/'+img_name, img_name,
                permission=False)"""
    os.system("rm *.htm")
    os.system("rm *.jpg")
    print("Uploaded", y, " graph(s) to gear.lafavre.us/Grant and index.html updated")
    s.show_message("Temp is "+it+"*C Pressure is "+ip+"bars Humidity is "+ih+"%",
                   text_colour=(150, 200, 150), back_colour=(0, 0, 0),
                   scroll_speed=(0.07))


#Program is Run here
try:
  client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
  client.on_connect = connect
  client.on_message = message
  client.connect()
  client.loop_blocking()
except KeyboardInterrupt:
  client.on_disconnect = disconnect

#upload.Delete('ftp.lafavre.us', 'gear@lafavre.us', 'Iotisnumber1!',
            #              'Grant', picture_list[loopLap-1])
