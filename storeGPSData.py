import mysql.connector
import os
import upload
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="project"
)
download = upload.Download()
clean = upload.Delete()
cursor = mydb.cursor()
os.chdir("busInfo")


"""
                clean.delete('', '', '',
                        '/Project', 'Bus7.txt')
"""
while True:
        try:
                """
                download.files('', '', '',
                               '/Project', '/var/www/html/busInfo/Bus7.txt', 'Bus7.txt')
                """
                fileNumber = len([os.listdir(".")])
                files = os.listdir(".")
                if fileNumber > 0:
                        for i in range(fileNumber):
                                with open(files[i], 'r') as f:
                                        info = f.readline()
                                        f = files[i]
                                        split1 = f.split(".")
                        bus = split1[0]
                        busNumber = bus.split("s")[1]
                        longitude = info.split("|")[0]
                        latitude = info.split("|")[1]
                        subState = info.split("|")[2]
                        timeState = info.split("|")[3]
                        state = info.split("|")[4]
                        sql = "UPDATE buses SET longitude="+str(longitude)+", latitude="+str(latitude)+", status='"+timeState+"', sub='"+subState+"', on_off="+str(state)+" WHERE busID="+str(busNumber)
                        val = (longitude, latitude)
                        cursor.execute(sql)
                        mydb.commit()
                        os.remove(files[i])
                        print("Database Updated and File Removed")
                else:
                        print("No files found")
        except KeyboardInterrupt:
                print("Exiting...")
                quit()
        except:
                print("Something went wrong...")
