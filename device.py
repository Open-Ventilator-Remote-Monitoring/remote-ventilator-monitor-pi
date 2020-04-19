class Device(object):
    def __init__(self, device_id: str, ventilator_alarm_sound_monitor: bool, ventilator_data_monitor: bool):
        self.device_id = device_id
        self.ventilator_alarm_sound_monitor = ventilator_alarm_sound_monitor
        self.ventilator_data_monitor = ventilator_data_monitor

    def get_device_id(self) -> str:
        return self.device_id

    def collecting_ventilator_data(self) -> bool:
        return self.ventilator_data_monitor

    def collecting_ventilator_alarm_sound(self) -> bool:
        return self.ventilator_alarm_sound_monitor
