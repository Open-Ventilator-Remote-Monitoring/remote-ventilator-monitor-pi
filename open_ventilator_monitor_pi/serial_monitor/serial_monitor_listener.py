from threading import Thread

from serial import Serial

from ventilator_communication import VentilatorCommunication


class SerialMonitorListener(Thread):
    def __init__(self, ventilator_communication: VentilatorCommunication, serial_connection: Serial):
        super(SerialMonitorListener, self).__init__()
        self.serial_connection = serial_connection
        self.ventilator_communication = ventilator_communication

    def run(self) -> None:

        count = 0
        header = b'\xff'

        while True:
            data = []
            x = self.serial_connection.read(1)
            if x == header:
                count+=1
            elif count == 2:
                count = 0
                length = ord(x)
                expected_checksum = length
                for i in range((length-1)//2):
                    right_byte = ord(self.serial_connection.read(1))
                    left_byte = ord(self.serial_connection.read(1))
                    int16 = (left_byte << 8) + right_byte
                    expected_checksum += int16
                    data.append(int16)

                checksum = self.serial_connection.read(1)
                expected_checksum = ~(expected_checksum%256)
                expected_checksum = expected_checksum.to_bytes(1, byteorder='big', signed=True)
                assert checksum == expected_checksum



