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

  ```reset_energy(slave_addr)``` : PZEM-004t have an internal energy counter, this function will rest it to 0Wh

```
>>> test.reset_energy(1)
```

Note: power precision is bound to 0.1_W resolution.
Depending on the application need it may be better to calculate it from voltage, 
current and power factor (P=UxIxPF) to get a better resolution:
```
  Voltage: 235.8_V
  Current: 0.086_A
  Power: 9.8_W
  Power calc: 9.733824
  Energy: 7_Wh
  Frequency: 50.0_Hz
  Power factor: 0.48
```

