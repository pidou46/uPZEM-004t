# uPZEM-004t

This repository consist of a micropython script to manage PZEM-004t powermeter device.

Most of the code is in the umodbus library.

I have made some minor changes the "timeout_char" have been changed from 10 to 2.
PZEM-004t seem's not to use timeout_char=10 #TO BE CHECKED A SECOND TIME



(2358, 87, 0, 99, 0, 11, 0, 500, 48, 0)

#response
#2353, 88, 0, 99, 0, 9, 0, 499, 48, 0
#Voltage value x0.1V = 235,3V
#Current value low 16 bits x0.001A = 0.088A
#Current value high 16 bits =0
#Power value low 16 bits x0.1W = 9,9W
#Power value high 16 bits =0
#Energy value low 16 bits x1Wh = 9Wh
#Energy value high 16 bits =0
#Frequency value x0.1Hz = 50,0Hz
#Power factor value x0.01 = 0.48
#Alarm status 0 = not alarm
