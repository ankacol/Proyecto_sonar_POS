from datetime import datetime, date, time
import os
from tkinter.constants import N
import os.path as path
import time

timeStampPos = []
nLocations = 0
ruta_archivo_pos = ""
posFreq = 1
var1 = 0

buffer_gtm = []

def get_pos(ruta_archivo_pos, check):
    ruta_salida = path.abspath(path.join(ruta_archivo_pos,".."))
    fsuperpos = open(ruta_salida + "/superpos.pos","w+")
    count = 0
    check = check
    
    secondsA = ""
    coordinatesA = ""
    coordinatesA1 = ""
    altitudA = ""
    secondsB = ""
    coordinatesB = ""
    coordinatesB1= ""
    altitudB = ""


    global timeStampPos
    global nLocations
    timeStamp = []
    nLocations = 0
    pos_size = os.path.getsize(ruta_archivo_pos)
    with open(ruta_archivo_pos, "r") as file_object:
        wait = True
        while wait:
            buffer = file_object.readline()
            if len(buffer) != 0:
                if buffer[0:7] == "%  GPST":
                    fsuperpos.write("%  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio\n")
                    buffer = "0"
                    while wait:
                        if  check == 0:
                            # print("estoy en normal")

                            if buffer == "0":
                                buffer = file_object.readline()
                            else:
                                buffer = buffer2
                            buffer2= file_object.readline()
                            if len(buffer2) != 0:
                                data_process(buffer, buffer2 ,fsuperpos )
                                
                            else:
                                fsuperpos.write(buffer)
                                wait = False
                            
                        else:
                            # print("estoy en reversed")
                            lines = file_object.readlines()
                            for buffer2 in reversed(lines):
                                if buffer == "0":
                                    buffer = file_object.readline()
                                else:
                                    buffer = buffer2
                                buffer2= file_object.readline()
                                if len(buffer2) != 0:
                                    data_process(buffer, buffer2 ,fsuperpos )
                                else:
                                    fsuperpos.write(buffer)
                                    wait = False
                            wait = False
                else:
                    if len(buffer) != 0:
                        fsuperpos.write(buffer)

            else:
                wait = False
    fsuperpos.close()
    
    if nLocations != 0:
        sorted(timeStamp, key=lambda x: x[0])
        timeStampPos = tuple(timeStamp)
    file_object.close()



def data_process(buffer, buffer2 ,fsuperpos ):
    
    sign = "-"

    secondsA = buffer[17:19]
    coordinatesA = buffer[25:38]
    coordinatesA1 = buffer[40:53]
    altitudA = buffer[56:64]

    secondsB = buffer2[17:19]
    coordinatesB = buffer2[25:38]
    coordinatesB1= buffer2[40:53]
    altitudB = buffer2[56:64]
    
    fsuperpos.write(buffer)

    coordinatesB = str(eval("(" + coordinatesA + "-" + coordinatesB + ")/4"))
    coordinatesB1 = str(eval("(" + coordinatesA1 + "-" + coordinatesB1 + ")/4"))
    altitudB = str(eval("(" + altitudA + "-" + altitudB + ")/4"))


    for i in  [0.251, 0.251, 0.251]:
        secondsA = float(secondsA)+i
        secondsB = str(secondsA)
        #si la longitud de los segundos es menor a 5 digitos se agrega un 0 para que guarde de manera correcta en el pos   NO 5.12 SI 05.12
        if len(secondsB) <= 5:
            secondsB = "0"+secondsB

        coordinatesA = str(eval(coordinatesA + sign + "(" + coordinatesB + ")"))
        coordinatesA1 = str(eval( coordinatesA1 + sign + "(" + coordinatesB1 + ")"))
        altitudA = str(eval(altitudA + sign + "(" + altitudB + ")"))

        # buffer_gtm[i] = buffer
        # print(buffer[0:17] + secondsB[0:2] + "." + secondsB[3:6] + buffer[23:25] + coordinatesB[0:13] + "  " + coordinatesB1[0:13] + "   " + altitudB[0:8] + buffer[64:142])
        # time.sleep(1)
        if secondsB[1] == ".":
            secondsB.replace(secondsB[1], secondsB[0])
            secondsB = "0"+secondsB
        fsuperpos.write(buffer[0:17] + secondsB[0:2] + "." + secondsB[3:6] + buffer[23:25] + coordinatesA[0:13] + "  " + coordinatesA1[0:13] + "   " + altitudA[0:8] + buffer[64:142])

        secondsA = secondsB
        coordinatesA = coordinatesA
        coordinatesA1 = coordinatesA1
        altitudA = altitudA
# fsuperpos.write(buffer2)
    