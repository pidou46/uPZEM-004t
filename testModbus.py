#modbus RTU

#nota: silence entre les trames: 3.5 carcteres, a caculer en fonction 
#XXXXbaud/10= character per second (1bit start + 8 bit + 1bit stop) 

PRESET = 0xFFFF
POLYNOMIAL = 0xA001 # bit reverse of 0x8005

READ_INPUT_REGISTER=b'x04'



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

def request_data(address):
    request = int(address).to_bytes(1, 'big') #address: 0x01-0xF7
    request += b'\x04' #function: read input register
    request += b'\x04' #function: read input register
    
    return data
    

# test case

#data = b'\xFF\x03\x02\x15\x28\x9F\x1E' # crc16() return 0 if CRC match
data = b'\xFF\x03\x02\x15\x28\x9F' # call crc16() without CRC octets to compute CRC

#\xFF: address (1 octet) : pzem-004t-v3.0: The address range of the slave is 0x01 ~ 0xF7. The address 0x00
#is used as the broadcas
#\x03: function (1 octet): pzem-004t-v3.0: 0x03 (Read Holding Register), 0x04 (Read Input Register), 0x06
#(Write Single Register), 0x41 (Calibration), 0x42 (Reset energy)
#\x02\x15\x28\x9F: data (0-252 octets)
#\x1E: crc (2 octets)

# master request : Slave Address + 0x04 + Register Address High Byte + Register Address Low Byte + Number
#of Registers High Byte + Number of Registers Low Byte + CRC Check High Byte + CRC Check
#Low Byte

# slave reply: Slave Address + 0x04 + Number of Bytes + Register 1 Data High Byte +
#Register 1 Data Low Byte + ... + CRC Check High Byte + CRC Check Low B




#error reply: Slave address + 0x84 + Abnormal code + CRC check high byte + CRC check
#low byte

#error codes: 0x01, Illegal function; 0x02, Illegal address; 0x03, Illegal data; 0x04, Slave error

crc = crc16(data)
print("CRC Test result: ", hex(crc), len(data))

