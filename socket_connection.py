import asyncio
import ssl
from queue import Queue
from threading import Lock, Thread

import websockets


class SocketConnection(Thread):
    lock: Lock

    def __init__(self, url: str, cert_info: ssl.SSLContext):
        super().__init__()
        self.cert_info = cert_info
        self.url = url
        self.message_queue = Queue()
        self.lock = Lock()

    async def main_loop(self, url):
        async with websockets.connect(url, ssl=self.cert_info) as connection:
            while True:
                if self.message_queue.qsize() > 0:
                    with self.lock:
                        while self.message_queue.qsize() > 0:
                            message = self.message_queue.get()
                            try:
                                print("sending ", message)
                                await connection.send(message)
                                await connection.recv()
                                print("sent")
                            except Exception as exp:
                                print("something broke", exp)

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.main_loop(url=self.url))

    def send_message(self, message):
        with self.lock:
            self.message_queue.put(message)
