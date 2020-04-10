from threading import Thread

from serial import Serial

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from ventilator_communication import VentilatorCommunication


class SerialMonitorListener(Thread):
    def __init__(self, ventilator_communication: VentilatorCommunication, serial_connection: Serial, serial_monitor_listener: SerialMonitorHandler):
        super(SerialMonitorListener, self).__init__()
        self.serial_connection = serial_connection
        self.ventilator_communication = ventilator_communication

    def read_int_16(self, serial_connection: Serial) -> int:
        right_byte = ord(self.serial_connection.read(1))
        left_byte = ord(self.serial_connection.read(1))
        return (left_byte << 8) + right_byte

    def run(self) -> None:

        count = 0
        header = b'\xff'

        while True:
            x = self.serial_connection.read(1)
            if x == header:
                count+=1
            elif count == 2:
                count = 0
                length = ord(x)
                expected_checksum = length
                ie_ratio = self.read_int_16(self.serial_connection)
                expected_checksum += ie_ratio
                peak_inspiratory_pressure = self.read_int_16(self.serial_connection)
                expected_checksum += peak_inspiratory_pressure
                tidal_volume = self.read_int_16(self.serial_connection)
                expected_checksum += tidal_volume
                respiratory_rate = self.read_int_16(self.serial_connection)
                expected_checksum += respiratory_rate
                peep = self.read_int_16(self.serial_connection)
                expected_checksum += peep

                checksum = self.serial_connection.read(1)
                expected_checksum = ~(expected_checksum%256)
                expected_checksum = expected_checksum.to_bytes(1, byteorder='big', signed=True)
                if checksum == expected_checksum:
                    self.




