import os
import time
def temp():
    while True: 
        os.chdir("/sys/bus/w1/devices/28-0000093bdc48")
        os.system("sudo modprobe w1-gpio")
        os.system("sudo modprobe w1-therm")
        with open("w1_slave", "r") as file1:
            tempfile = file1.read()
        file1_line2 = tempfile.split("\n")[1]
        tempnumber = file1_line2.split(" ")[9]
        tempfirst = float(tempnumber[2:])
        tempfirst = tempfirst / 1000
        temp1 = float(tempfirst)
        os.chdir("/sys/bus/w1/devices/28-0000093c4df3")
        with open("w1_slave", "r") as file2:
            tempfile2 = file2.read()
        file2_line2 = tempfile2.split("\n")[1]
        tempnumber2 = file2_line2.split(" ")[9]
        tempfirst2 = float(tempnumber2[2:])
        tempfirst2 = tempfirst2 / 1000
        temp2=float(tempfirst2)
        temp1 = temp1*1.8+32
        temp2 = temp2*1.8+32
        temp1 = round(temp1, 2)
        temp2 = round(temp2, 2)
        realtemp=(temp1+temp2) / 2
        realtemp = round(realtemp, 2)
        return realtemp
print(temp())
