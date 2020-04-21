class AlarmData(object):
    def __init__(self, status: bool, timestamp: float):
        self.status = status
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def get_status(self):
        return self.status
