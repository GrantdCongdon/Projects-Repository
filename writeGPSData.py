import gps
from time import sleep
import time
import os
import RPi.GPIO as g
import upload
from Hologram.HologramCloud import HologramCloud
credentials = {'devicekey': 'i%F6vH)('}
hologram = HologramCloud(credentials, network='cellular')
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
os.chdir("busInfo")
export = upload.Upload()
g.setmode(g.BCM)
g.setwarnings(True)
g.setup(4, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(18, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(17, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(27, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(21, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(23, g.IN, pull_up_down=g.PUD_DOWN)
subYes = 0
subNo = 0
busLate = 0
busEarly = 0
busOnTime = 0
trackerActive = True
def longitude():
    global session
    x=0
    lon=[]
    lonTotal=0.0
    try:
        while x<5:
            report = session.next()
            #print(report)
            if report['class'] == 'TPV':
                if hasattr(report, 'lat'):
                    lon.append(report.lon)
                    gpsTime = report.time
            sleep(1)
            x=x+1
        for i in range(len(lon)):
            #print(i)
            lonTotal=lon[i]+lonTotal
        finalLongitude = lonTotal/len(lon)
        finalLongitude = str(finalLongitude)
        return finalLongitude, gpsTime
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")

def latitude():
    global session
    x=0
    lat=[]
    latTotal=0.0
    try:
        while x<5:
            report = session.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'lon'):
                    lat.append(report.lat)
                    gpsTime = report.time
            sleep(1)
            x=x+1
        for i in range(len(lat)):
            latTotal=lat[i]+latTotal
        finalLatitude = latTotal/len(lat)
        finalLatitude = str(finalLatitude)
        return finalLatitude, gpsTime
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")
def gpsTime():
    global session
    x=0
    try:
        while x<5:
            report = session.next()
            if report['class'] == 'TPV':
                      gpsTime = report.time
            sleep(1)
            x=x+1
        return gpsTime
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")
while True:
    try:
        print("Press button that determines if sub and status")
        sleep(3)
        print("Too late if you are not pressin the buttons")
        inputStateSub = g.input(4)
        #inputStateSubNo = g.input(18)
        inputStateBusTime = g.input(21)
        #inputStateBusOnTime = g.input(27)
        #inputStateBusLate = g.input(17)
        
        inputStateTrackerActive = g.input(23)
        
        if inputStateSub == g.HIGH:
            subYes = 1
            subNo = 0
        elif (inputStateSub == g.HIGH) and (sub == 1):
            subYes = 0
            subNo = 1
        else:
            if subNo == 1:
                subYes = 0
                subNo = 1
            else: 
                subYes = 1
                subNo = 0
        
        if inputStateBusTime == g.HIGH and (busOnTime == 0) and (busLate == 0):
            busEarly = 1
            busOnTime = 0
            busLate = 0
        elif (inputStateBusTime == g.HIGH) and (busEarly==0) and (busLate==0):
            busEarly = 0
            busOnTime = 1
            busLate = 0
        elif (inputStateBusTime == g.HIGH) and (busEarly==0) and (busOnTime==0):
            busEarly = 0
            busOnTime = 0
            busLate = 1
        else:
            if busEarly == 1:
                busEarly = 1
                busOnTime = 0
                busLate = 0
            elif busOnTime == 1:
                busEarly = 0
                busOnTime = 1
                busLate = 0
            else:
                busEarly = 0
                busOnTime = 0
                busLate = 1
        
        if inputStateTrackerActive == g.HIGH:
            trackerActive = False
        elif (inputStateTrackerActive == g.HIGH) and (trackerActive==False):
            trackerActive = True
        else:
            if trackerActive:
                trackerActive = True
            else:
                trackerActive = False
        if int(time.strftime("%H")) >= 17:
            trackerActive = False
        print("You can stop pressing the buttons now")
        with open("Bus7.txt", "w") as f:
            f.write(longitude()[0]+"|")
            f.write(latitude()[0]+"|")
            if subYes == 1:
                f.write("Yes|")
                print("Sub Exists")
            elif subNo == 1:
                f.write("No|")
                print("Sub dant exist")
            else:
                print("Something is wrong")
                      
            if busEarly == 1:
                f.write("Early|")
                print("Bus is running early")
            elif busOnTime == 1:
                f.write("On Time|")
                print("Bus is on time")
            elif busLate == 1:
                f.write("Late|")
                print("Bus is running late")
            else:
                print("Something is wrong")
            
            if trackerActive:
                f.write('1')
                print("Bus Locator is active")
            else:
                f.write('0')
                print("Bus locator is off")
                
            f.flush()
        hologram.network.connect(timeout=10)
        """
        export.files('', '', '',
                     '/Project', '/var/www/html/busInfo/Bus7.txt', 'Bus7.txt')
        os.remove("Bus.txt")
        """
        hologram.network.disconnect()
        print("Updated GPS File")
        sleep(1)
    except KeyboardInterrupt:
        with open("Bus7.txt", "w") as f:
            f.write("NULL|NULL|NULL|NULL|0")
            f.flush()
        """
        export.files('', '', '',
                     '/Project', '/var/www/html/busInfo/Bus7.txt', 'Bus7.txt')
        os.remove("Bus7.txt")
        """
        print("Exiting...")
        quit()
    except:
        print("Something went wrong")
