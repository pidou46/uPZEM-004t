"""micropython library to manage PZEM_004t_V3.0 (AC measuring device)"""

import uModBusSerial, json, time
import uModBusFunctions
import uModBusConst
import struct

class uPZEM(uModBusSerial.uModBusSerial):
    """pins order [tx,rx]"""
    def __int__(self,uart_id, baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=None, ctrl_pin=None):
        self.super(uart_id, baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=None, ctrl_pin=None)
    
    #overrided method from uModBusSerial with data conversion and data packing in json string
    def read_input_registers(self, slave_addr, starting_address=0, register_quantity=10, signed=True):
        register_value=list(range(6))
        modbus_pdu = uModBusFunctions.read_input_registers(starting_address, register_quantity)
      
        resp_data = self._send_receive(modbus_pdu, slave_addr, True)

        register_value[0]=int.from_bytes(resp_data[0:2],'big') * 0.1 #1LSB 0.1V
        register_value[1]=(int.from_bytes(resp_data[2:4],'big') \
                 + int.from_bytes(resp_data[4:6],'big')*65536) \
                 * 0.001 #1LSB 0.001A
        register_value[2]=(int.from_bytes(resp_data[6:8],'big') \
                 + int.from_bytes(resp_data[8:10],'big')*65536) \
                 * 0.1 #1LSB 0.1W
        register_value[3]=(int.from_bytes(resp_data[10:12],'big') \
                 + int.from_bytes(resp_data[12:14],'big')*65536) \
                 * 1 #1LSB 1Wh
        register_value[4]=int.from_bytes(resp_data[14:16],'big') * 0.1 #1LSB 0.1Hz
        register_value[5]=int.from_bytes(resp_data[16:18],'big') * 0.01 #1LSB 0.01V

        return json.dumps(register_value)

    def reset_energy(self, slave_addr):
        """pdu specific to PZEM (non modbus standard) to rest energy counter"""
        pdu=struct.pack('>BHH', 0X42)
        self._send_receive(pdu, 1, False)
    


if __name__=="__main__":
    counter_grid=uPZEM(1,pins=[12,13])
    data=json.loads(counter_grid.read_input_registers(1))
    print("Voltage: {}_V".format(data[0]))
    print("Current: {}_A".format(data[1]))
    print("Power: {}_W".format(data[2]))
    print("Power calc: {}".format(data[0]*data[1]*data[5]))
    print("Energy: {}_Wh".format(data[3]))
    print("Frequency: {}_Hz".format(data[4]))
    print("Power factor: {}".format(data[5]))


#test=bytearray(b'\t%\x00Z\x00\x00\x00d\x00\x00\x00\x19\x00\x00\x01\xf4\x00/\x00\x00')

#len(test)
#20
#struct.unpack('>hhhhhhhhhh',test)
#(2341, 90, 0, 100, 0, 25, 0, 500, 47, 0)
    




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


