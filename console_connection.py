from ventilator_communication import VentilatorCommunication


class ConsoleConnection(VentilatorCommunication):
    def __init__(self, link: str, baud: int, timeout: int) -> None:
        print(f'Connecting on {link} at baud {baud} with timeout {timeout}')

    def start_connection(self) -> None: pass

    def send_message(self, byte_string: bytes) -> None:
        print(byte_string.decode('utf-8'))

    def read_line(self) -> bytes:
        print('Request Came in, enter reply')
        return input().encode('utf-8')
