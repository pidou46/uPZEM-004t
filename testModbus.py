"""micropython library to manage PZEM_004t_V3.0 (AC measuring device)"""

from machine import UART


#crc16 constants valide for modbus-RTU
PRESET = 0xFFFF
POLYNOMIAL = 0xA001 # bit reverse of 0x8005

#pzem-004t specific

#Modbus-RTU functions codes
READ_HOLDING_REGISTER = 0x03
READ_INPUT_REGISTER = 0x04
WRITE_SINGLE_REGISTER = 0x06
CALIBRATION = 0x41 #only address supported 0xF8, password 0x3721
RESET_ENERGY = 0x42


#register definition
VOLTAGE = 0x0000 #1LSB = 0.1_V
CURRENT_LOW = 0x0001 #low 16_bits (1LSB = 0.001_A)
CURRENT_HIGH = 0x0001 #high 16_bits
POWER_LOW = 0x0002 #low 16_bits (1LSB = 0.1_W)
POWER_HIGH = 0x0003 #high 16_bits
ENERGY_LOW = 0x0002 #low 16_bits (1LSB = 1_Wh)
ENERGY_HIGH = 0x0003 #high 16_bits
FREQUENCY = 0x0007 #1LSB = 0.1_Hz
POWER_FACTOR = 0x0008 #1LSB = 0.01
ALARM_STATUS = 0x0009 #0xFFFF alarm set, 0x0000 alarm not set

#errors
ILLEGAL_FUNCTION = 0x01
ILLEGAL_ADDRESS = 0x02
ILLEGAL_DATA = 0x03
SLAVE_ERROR = 0x04

def crc16(data):
    crc = PRESET
    for c in data:
        crc = crc ^ c
        for j in range(8):
            if crc & 0x01:
                crc = (crc >> 1) ^ POLYNOMIAL
            else:
                crc = crc >> 1
    return crc


class uPZEM():
    id_counter=0
    
    def __init__(self,address,tx=None,rx=None):
        uPZEM.id_counter+=1
        self.id=uPZEM.id_counter
        try:
            assert 0x01 <= address <= 0xF7
            self.address=address
            #create uart
            uart = UART(self.id,9600)
            uart.init(9600, tx=, rx=, bits=8, parity=None, stop=1) #UART to RS485 communication interface: Baud rate is 9600, 8 data bits, 1 stop bit, no parity
        except AssertionError:
            print("Address out of range 1-247")
            raise
        except:
            print("UART error")


    def request_data():
        
        #build request
        request = self.address.to_bytes(1, 'big') #convert address in bytes
        request += b'\x04' #function: read input register
        request += b'\x00' #register address high byte
        request += b'\x00' #register address low byte
        request += b'\x00' #number of register high byte
        request += b'\x0A' #number of register low byte (all 10 registers)
        request += crc16(request).to_bytes(2,'big') #add crc bytes (2)
        
        
        #send request
        
        #compute power from actual voltage, current and power factor gives higer precision than direct power register
        
        #parse returned values in a list with timestamp
        
       
        return data
    

if __name__=="__main__":
    
    grid = uPZEM(address=0x01,tx=12,rx=13)
    grid_data = grid.request_data()
    
    
# test case

#data = b'\xFF\x03\x02\x15\x28\x9F\x1E' # crc16() return 0 if CRC match
data = b'\xFF\x03\x02\x15\x28\x9F' # call crc16() without CRC octets to compute CRC

#\xFF: address (1 octet) : Address range of the slave is 0x01 ~ 0xF7. The address 0x00
#is used as the broadcast
#\x03: function (1 octet)
#\x02\x15\x28\x9F: data (0-252 octets)
#\x1E: crc (2 octets)

# master request : Slave Address + 0x04 + Register Address High Byte + Register Address Low Byte + Number
#of Registers High Byte + Number of Registers Low Byte + CRC Check High Byte + CRC Check
#Low Byte

# slave reply: Slave Address + 0x04 + Number of Bytes + Register 1 Data High Byte +
#Register 1 Data Low Byte + ... + CRC Check High Byte + CRC Check Low B


#error reply: Slave address + 0x84 + Abnormal code + CRC check high byte + CRC check
#low byte

#nota: silence entre les trames: 3.5 carcteres, a caculer en fonction 
#XXXXbaud/10= character per second (1bit start + 8 bit + 1bit stop) 

#request_data(200)

crc = crc16(data)
print("CRC Test result: ", hex(crc), len(data))

