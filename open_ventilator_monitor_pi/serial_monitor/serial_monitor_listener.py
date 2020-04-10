from threading import Thread

from serial import Serial

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from ventilator_communication import VentilatorCommunication, VentilatorData


class SerialMonitorListener(Thread):
    def __init__(self, ventilator_communication: VentilatorCommunication, serial_connection: Serial, serial_monitor_handler: SerialMonitorHandler):
        super(SerialMonitorListener, self).__init__()
        self.serial_connection = serial_connection
        self.ventilator_communication = ventilator_communication
        self.serial_monitor_handler = serial_monitor_handler

    def _read_int_16(self) -> int:
        right_byte = ord(self.serial_connection.read(1))
        left_byte = ord(self.serial_connection.read(1))
        return (left_byte << 8) + right_byte

    def run(self) -> None:

        count = 0
        header = b'\xff'

        while True:
            x = self.serial_connection.read(1)
            if x == header:
                count += 1
            # if the second header isn't a header it resets back
            elif count == 1:
                count = 0
            elif count == 2:
                count = 0
                length = ord(x)
                expected_checksum = length
                ie_ratio = self._read_int_16()
                expected_checksum += ie_ratio
                peak_inspiratory_pressure = self._read_int_16()
                expected_checksum += peak_inspiratory_pressure
                tidal_volume = self._read_int_16()
                expected_checksum += tidal_volume
                respiratory_rate = self._read_int_16()
                expected_checksum += respiratory_rate
                peep = self._read_int_16()
                expected_checksum += peep

                checksum = self.serial_connection.read(1)
                expected_checksum = ~(expected_checksum%256)
                expected_checksum = expected_checksum.to_bytes(1, byteorder='big', signed=True)
                if checksum == expected_checksum:
                    self.serial_monitor_handler.update(VentilatorData(
                        tidal_volume=tidal_volume,
                        respirator_rate=respiratory_rate,
                        peak_inspiratory_pressure=peak_inspiratory_pressure,
                        ie_ratio=ie_ratio,
                        peep=peep,
                        alarms={}
                    ))




