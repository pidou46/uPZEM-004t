import uModBusSerial
#pins [tx,rx]
serial=uModBusSerial.uModBusSerial(1,pins=[12,13,-1,-1])

data = serial.read_input_registers(1,0,10)
#data = serial.read_coils(1,0,10)

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
print(data)