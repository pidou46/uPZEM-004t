#import uasyncio as asyncio
import asyncio
import struct


#crc16 constants valid for modbus-RTU
PRESET = 0xFFFF
POLYNOMIAL = 0xA001 # bit reverse of 0x8005

class PZEM:
    def __init__(self,address=0x01):
        #compute crc16 request for actual address and build request to save time later
        try:
            assert 0x01 <= address <= 0xF7
            self.address=address
        except AssertionError:
            print("Address out of range 1-247")
            raise
        except:
            print("Wrong address")


    def __aiter__(self):  # needed to act as an iterator
        return self

    async def __anext__(self):
        await asyncio.sleep(1)
        #msg = await self.uart.read()
        msg=crc16(b'\x01\x04\x00\x00\x04')
        return msg

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


        
if __name__=="__main__":
    #create uart
    #uart = UART(self.id,9600)
    #uart.init(9600, tx=16, rx=17, bits=8, parity=None, stop=1) #UART to RS485 communication interface: Baud rate is 9600, 8 data bits, 1 stop bit, no parity


    pzem = PZEM(0x02)

    async def run():
        async for x in pzem:
            print(x)

    asyncio.run(run())
    