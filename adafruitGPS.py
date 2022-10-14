import gps
from time import sleep
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat'):
                print(report.time)
                print("Latitude: "+str(report.lat))
                print("Longitude: "+str(report.lon))
        sleep(2)
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")
