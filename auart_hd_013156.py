# auart_hd.py
# Author: Peter Hinch
# Copyright Peter Hinch 2018-2020 Released under the MIT license

# Demo of running a half-duplex protocol to a device. The device never sends
# unsolicited messages. An example is a communications device which responds
# to AT commands.
# The master sends a message to the device, which may respond with one or more
# lines of data. The master assumes that the device has sent all its data when
# a timeout has elapsed.

# In this test a physical device is emulated by the Device class
# To test link X1-X4 and X2-X3

from machine import UART
import uasyncio as asyncio
from primitives.delay_ms import Delay_ms

#crc16 constants valid for modbus-RTU
PRESET = 0xFFFF
POLYNOMIAL = 0xA001 # bit reverse of 0x8005


class PZEM():
    def __init__(self, uart, address=0x01, timeout=1000):
        self.uart = uart
        self.uart.init(baudrate=9600,bits=8,parity=None,stop=1)
        self.timeout = timeout
        self.swriter = asyncio.StreamWriter(self.uart, {})
        self.sreader = asyncio.StreamReader(self.uart)
        self.delay = Delay_ms()
        self.response = ""
        #build data request with address of the device at cronstruction time to avoid crc calculation later.
        self.request = bytes('','utf-8') + bytes([address]) + bytes('\x04\x00\x00\x04','utf-8')
        self.request += crc16(request)
        asyncio.create_task(self._send())
        asyncio.create_task(self._recv())

    async def _send(self):
        while True:
            await pzem.send_command(self.request)
            await asyncio.sleep(1) #delay between request to be addded as a parameter in constructor


    async def _recv(self):
        while True:
            res = await self.sreader.read(40) # the device does not send ed of line, so I read some data. TODO: testing -1
            self.delay.trigger(self.timeout)  # Got something, retrigger timer

    async def send_command(self, command):
        self.response = ""  # Discard any pending messages
        if command is None:
            print('Timeout test.')
        else:
            await self.swriter.awrite("{}\r\n".format(command))
            print('Command sent:', command)
        self.delay.trigger(self.timeout)  # Re-initialise timer
        while self.delay.running():
            await asyncio.sleep(1)  # Wait for 4s after last msg received
        return self.response
    
def crc16(data):
    crc = PRESET
    for c in data:
        crc = crc ^ c
        for j in range(8):
            if crc & 0x01:
                crc = (crc >> 1) ^ POLYNOMIAL
            else:
                crc = crc >> 1
    return struct.pack('<H',crc)

async def main():
    uart=UART(1)
    pzem = PZEM(uart,address=0x01)

        


if __name__=="__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
        print('as_demos.auart_hd.test() to run again.')

