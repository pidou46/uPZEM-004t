# uPZEM-004t

This repository consist of a micropython script to manage PZEM-004t powermeter device.

Hardware:
- esp32
    connect tx to pin 12 and rx to pin 13
- PZEM-004t V3
    add 1khom resitor between 5V and CT 81 7C
    
firmware: 
micropython V1.12



Most of the code is in the umodbus library.

Warning: read_input_registers return 
"Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
  File "uModBusSerial.py", line 155, in read_input_registers
  File "uModBusSerial.py", line 106, in _send_receive
  File "uModBusSerial.py", line 111, in _validate_resp_hdr
OSError: no data received from slave"
    
When to power side of the PZEM-004t is unpluged

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


request "read_input_registers" takes about : 100_ms
