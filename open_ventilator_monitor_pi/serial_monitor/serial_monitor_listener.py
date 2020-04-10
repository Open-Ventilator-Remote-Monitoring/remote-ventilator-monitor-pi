from threading import Thread

from serial import Serial, SerialTimeoutException

from open_ventilator_monitor_pi.serial_monitor.serial_monitor_handler import SerialMonitorHandler
from ventilator_communication import VentilatorCommunication, VentilatorData


class SerialMonitorListener(Thread):
    def __init__(self, ventilator_communication: VentilatorCommunication, serial_connection: Serial, serial_monitor_handler: SerialMonitorHandler):
        super(SerialMonitorListener, self).__init__()
        self.serial_connection = serial_connection
        self.ventilator_communication = ventilator_communication
        self.serial_monitor_handler = serial_monitor_handler
        self.is_running = False

    def _read_byte(self) -> bytes:
        while True:
            first_byte = self.serial_connection.read(1)
            if first_byte:
                return first_byte

    def _read_int_8(self) -> int:
        first_byte = self._read_byte()
        return ord(first_byte)

    def _read_int_16(self) -> int:
        right_byte = self._read_byte()
        left_byte = self._read_byte()
        return (ord(left_byte) << 8) + ord(right_byte)

    def _calc_checksum_int_16(self, value: int) -> int:
        return (value & 0xFF) + (value >> 8 & 0xFF)

    def stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        count = 0
        header = ord(b'\xff')
        while self.is_running:
            try:
                x = self._read_int_8()
                if count == 2:
                    count = 0
                    length = x
                    expected_checksum = length
                    ie_ratio = self._read_int_16()
                    expected_checksum += self._calc_checksum_int_16(ie_ratio)
                    peak_inspiratory_pressure = self._read_int_16()
                    expected_checksum += self._calc_checksum_int_16(peak_inspiratory_pressure)
                    tidal_volume = self._read_int_16()
                    expected_checksum += self._calc_checksum_int_16(tidal_volume)
                    respiratory_rate = self._read_int_16()
                    expected_checksum += self._calc_checksum_int_16(respiratory_rate)
                    peep = self._read_int_16()
                    expected_checksum += self._calc_checksum_int_16(peep)

                    checksum = self._read_int_8()
                    if expected_checksum & checksum == 0:
                        self.serial_monitor_handler.update(VentilatorData(
                            tidal_volume=tidal_volume,
                            respirator_rate=respiratory_rate,
                            peak_inspiratory_pressure=peak_inspiratory_pressure,
                            ie_ratio=ie_ratio,
                            peep=peep,
                            alarms={}
                        ))
                elif x == header:
                    count += 1
                # if the second header isn't a header it resets back
                elif count == 1:
                    count = 0
            except SerialTimeoutException:
                continue




