# uPZEM-004t

micropython library to manage PZEM_004t_V3.0 (AC measuring device)


This library have been tested with ESP32 microcontroler and offical micropython firmware.

## Hardware mod
Voltage level on the serial port of the PZEM-004t is 5v.
It need to be lowered to 3.3v to communicate with ESP32.
The easiest way to do it is to add a 1khom resitance between the 5V pin of the connectign port and the closet pin to U3 symbol.

## Install
This library is dependent upon uModBus library: https://github.com/techbase123/micropython-modbus

Clone this repository and copy the files on your device.

## Usage:

Not every PZEM-004t functions have been implemented, only the following:

  ```read_input_registers(slave_addr)``` : it will return a tupple with: Voltage(V), Current(A), Power(W), Energy(Wh), Frequency(Hz), Power factor
  
```
>>> import uPZEM_004t
>>> test=uPZEM_004t_0_0_4.uPZEM(1,pins=[12,13])
>>> test.read_input_registers(1)
'[233.6, 0.08700001, 9.8, 11, 50.0, 0.48]'
```
You will the following error if the device is not conencted to AC power ```OSError: no data received from slave```



  ```reset_energy(slave_addr)``` : PZEM-004t have an internal energy counter, this function will rest it to 0Wh

```
>>> test.reset_energy(1)
```

Memory usage:
```
>>> use: 160
```


Note: power precision is bound to 0.1_W resolution.
Depending on the application need it may be better to calculate it from voltage, 
current and power factor (P=UxIxPF) to get a better resolution:
```
  Voltage: 235.8_V
  Current: 0.086_A
  Power factor: 0.48
  Power: 9.8_W
  Power calc: 9.733824
```

##Todo:

I used modbus lib mainly because of CRC16 calculation, but it seems to be a lighter way to do it :

https://forum.micropython.org/viewtopic.php?f=15&p=54928&sid=fd4c4c060a64d3abae86685bd1c0bda6#p54928

"And another one makes it even faster on rp2040, replacing the multiplication by shift and subtraction. On RP2040 from 3.3ms to 1.9 ms.

Code: Select all
```
@micropython.native
def hash(str):
    result = 0xceedpulling

    for v in str:
        result = ((result << 7) - result + v) & 0xffff
    return result
```
The problem is here the missing support for hardware multiplication in the firmware. That was already addressed.
On ESP32 you can write:
result = (result *127 + v) & 0xffff
The code looks now pretty similar to the table based CRC16. Only it uses less RAM and is somewhat faster,"

This would be intrusting to test it and see howmuch ram to could save and if it can increase pulling frequency
