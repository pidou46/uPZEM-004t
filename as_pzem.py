import uasyncio as asyncio
from machine import UART
from time import sleep
import struct

#crc16 constants valide for modbus-RTU
PRESET = 0xFFFF
POLYNOMIAL = 0xA001 # bit reverse of 0x8005

#Modbus-RTU functions codes
READ_HOLDING_REGISTER = 0x03
READ_INPUT_REGISTER = 0x04
WRITE_SINGLE_REGISTER = 0x06
CALIBRATION = 0x41 #only address supported 0xF8, password 0x3721
RESET_ENERGY = 0x42
WRITE_MODBUS_ADDRESS = 0x0002 #range is 0x0001~0x00F7

class PZEM004T:
    def __init__(self, uart, address):
        
        self.uart=uart
        self.address=int.to_bytes(address,1,'big')
        
        self.request = int.to_bytes(address,1,'big') #address on modbus: int.to_bytes(1, 1,'big') #convert address in bytes
        self.request += int.to_bytes(READ_INPUT_REGISTER,1,'big') #function: read input register
        self.request += b'\x00' #register address high
        self.request += b'\x00' #register address low byte
        self.request += b'\x00' #number of register high byte
        self.request += b'\x0A' #number of register low byte (all 10 registers)

        self.request += crc16(self.request)
        
    async def sender(self):
        swriter = asyncio.StreamWriter(self.uart, {})
        while True:
            swriter.write(self.request)
            await swriter.drain()
            await asyncio.sleep(2)

    async def receiver(self):
        print("receiver")
        sreader = asyncio.StreamReader(self.uart)
        while True:
            res = await sreader.read(40)
            print('Received', res)
            print_received(res)
    
    def resetEnergyCounter(self):
        request=self.address
        request+=int.to_bytes(RESET_ENERGY,1,'big')
        request += crc16(request)
        
        self.uart.write(request)

        sleep(0.1)

        return self.uart.read(40)
        
    def setAddress(self, new_address):
        
        new_address=int.to_bytes(new_address,1,'big')
        
        if self.address==new_address:
            print(f'address already set to {self.address}')
            return    
        
        request=self.address
        request+=int.to_bytes(WRITE_SINGLE_REGISTER,1,'big')
        request+=int.to_bytes(WRITE_MODBUS_ADDRESS,1,'big')
        reqeust+=b'\x00'
        request+=new_address
        request += crc16(request)
        
        self.uart.write(request)

        sleep(0.1)

        response=self.uart.read(40)
        
        print(f"response: {response}") #response: b'\x02\x06\x00\x02\x00\x03h8'
        if response[1:2]==b'\x86':
            raise Exception('Error setting address')
        else:
            self.address=new_address
            
        
    
    async def run_forever(self):
        while True:
            await asyncio.sleep(1)

    def run(self):
        asyncio.create_task(self.sender())
        asyncio.create_task(self.receiver())


def scan(uart):
    print("search for device on modbus...")
    slaves=[]
    for address in range(0,247):
        response=check_address(uart,address)
        if response!=None:
            slaves.append(response)
        
    print(f"Found device at address: {slaves}")
    return slaves

def check_address(uart,address):
    request=int.to_bytes(address,1,'big')
    request+=b'\x03\x00\x02\x00\x01'
    request += crc16(request)
    
    uart.write(request)

    sleep(1)

    response=uart.read(40)
    if response==None:
        return None
    if response[4:5]==int.to_bytes(address,1,'big'):
        return address
    

def print_received(res):
    data=[0]*6
    data[0]=int.from_bytes(res[3:5],'big') * 0.1 #1LSB 0.1V - tension
    data[1]=(int.from_bytes(res[5:7],'big') \
                 + int.from_bytes(res[7:8],'big')*65536) \
                 * 0.001 #1LSB 0.001A - Current
    data[2]=(int.from_bytes(res[9:11],'big') \
                 + int.from_bytes(res[11:13],'big')*65536) \
                 * 0.1 #1LSB 0.1W - Power
    data[3]=(int.from_bytes(res[13:15],'big') \
                 + int.from_bytes(res[15:17],'big')*65536) \
                 * 1 #1LSB 1Wh - Energy
    data[4]=int.from_bytes(res[17:19],'big') * 0.1 #1LSB 0.1Hz - frequency
    data[5]=int.from_bytes(res[19:21],'big') * 0.01 #1LSB 0.01 - power factor

    print("Voltage: {}_V".format(data[0]))
    print("Current: {}_A".format(data[1]))
    print("Power: {}_W".format(data[2]))
    #print("Power calc: {}".format(data[0]*data[1]*data[5]))
    print("Energy: {}_Wh".format(data[3]))
    print("Frequency: {}_Hz".format(data[4]))
    print("Power factor: {}".format(data[5]))



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


async def run_forever():
    while True:
        await asyncio.sleep(1)


#Boilerplate code from petterhinch async tutorial
#https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#511-global-exception-handler

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)



async def main():
    set_global_exception()  # Debug aid
    
    uart = UART(2, 9600, bits=8, parity=None, stop=1, timeout=0, tx=16, rx=17)

    first = PZEM004T(uart,3)  # Constructor might create tasks
    first.run()
    await first.run_forever()  # Non-terminating method
    



if __name__=="__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop() # Clear retained state

