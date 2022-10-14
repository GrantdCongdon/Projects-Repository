#Libraries
import os
import time
from ftplib import FTP_TLS
#Universal Variable
x=1
tt=0
temp_list = []
#Functions
def gettime():
    timenow = time.strftime("%H:%M")
    return timenow
def file_setup(filename):
    header = ["temp", "date", "time"]
    with open(filename, "w") as f:
        f.write(",".join(str(value) for value in header) + "\n")
def read_sensor1():
    os.system("sudo modprobe w1-gpio")
    os.system("sudo modprobe w1-therm")
    time1 = time.strftime("%H:%M")
    os.chdir("/sys/bus/w1/devices/28-0000093bdc48")
    with open("w1_slave", "r") as file1:
        tempfile = file1.read()
    file1_line2 = tempfile.split("\n")[1]
    tempnumber = file1_line2.split(" ")[9]
    tempfirst = float(tempnumber[2:])
    tempfirst = tempfirst / 1000
    temp1 = float(tempfirst)
    t1 = str(temp1)
    os.chdir("/home/pi/python")
    return time1, t1
def read_sensor2():
    os.system("sudo modprobe w1-gpio")
    os.system("sudo modprobe w1-therm")
    time2 = time.strftime("%H:%M")
    os.chdir("/sys/bus/w1/devices/28-0000093c4df3")
    with open("w1_slave", "r") as file2:
        tempfile2 = file2.read()
    file2_line2 = tempfile2.split("\n")[1]
    tempnumber2 = file2_line2.split(" ")[9]
    tempfirst2 = float(tempnumber2[2:])
    tempfirst2 = tempfirst2 / 1000
    temp2=float(tempfirst2)
    t2 = str(temp2)
    os.chdir("/home/pi/python")
    return t2
def combine_sensor():
    sense_data = []
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    temp1 = read_senor1()
    temp2 = read_sensor2()
    sense_data.append(temp1, temp2, time)
y1 = read_sensor1()[1]
time1 = read_sensor1()[0]
time.sleep(58)
y2 = read_sensor1()[1]
time2 = read_sensor1()[0]
time.sleep(58)
y3 = read_sensor1()[1]
time3 = read_sensor1()[0]
time.sleep(58)
y4 = read_sensor1()[1]
time4 = read_sensor1()[0]
time.sleep(58)
y5 = read_sensor1()[1]
time5 = read_sensor1()[0]
date = time.strftime("%D")
with open("temp.htm", "w") as t:
    t.write('<!doctype html>\n')
    t.write('<html>\n<head>\n')
    t.write('<meta charset="UTF-8">\n')
    t.write('<title>HAT Weather Station</title>\n')
    t.write('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n')
    t.write('<script type="text/javascript">\n')
    t.write('google.charts.load("current", {"packages":["corechart"]});\n')
    t.write('google.charts.setOnLoadCallback(drawChart);\n')
    t.write('function drawChart() {\n')
    t.write('var data = google.visualization.arrayToDataTable([\n')
    t.write('["Time", "Temp"],\n')
    t.write('[' + '"' + time1 + '"' + ', ')
    t.write(y1 + '],\n')
    t.write('[' + '"' +  time2 + '"' + ', ')
    t.write(y2 + '],\n')
    t.write('[' + '"' + time3 + '"' + ', ')
    t.write(y3 + '],\n')
    t.write('[' + '"' + time4 + '"' ', ')
    t.write(y4 + '],\n')
    t.write('[' + '"' + time5 + '"' + ', ')
    t.write(y5 + '],\n')
    t.write(']);\n')
    t.write('var options = {\n')
    t.write('title: "Gear Weather Station for ' + date +'",\n')
    t.write('curveType: "function",\nlegend: { position: "bottom" }\n')
    t.write('};\n')
    t.write('var chart = new\n')
    t.write('google.visualization.LineChart(document.getElementById("curve_chart")\n')
    t.write(');\n')
    t.write('chart.draw(data, options);\n}\n')
    t.write('</script>\n')
    t.write('</head>\n')
    t.write('<body>\n')
    t.write('<div id="curve_chart" style="width: 900px; height: 500px">\n')
    t.write('<div>')
    t.write('</body>')
    t.write('</html>')
import connect
connect.Upload('', '', '', 'Grant',
               '/home/pi/python/temp.htm', "temp.htm")
print("Done")
