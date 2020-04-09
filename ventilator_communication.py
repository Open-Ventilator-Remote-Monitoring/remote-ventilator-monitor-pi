class VentilatorCommunication:
    def start_connection(self) -> None: pass

    def send_message(self, byte_string: bytes) -> None: pass

    def read_line(self) -> bytes: pass

    def request(self, command: str) -> str:
        self.send_message(command.encode('utf-8'))
        return self.read_line().decode('utf-8').rstrip()
