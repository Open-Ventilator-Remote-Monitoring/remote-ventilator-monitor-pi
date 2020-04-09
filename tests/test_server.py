from unittest import TestCase, mock


class Test(TestCase):
    def setUp(self) -> None:
        with mock.patch('serial_service.SerialService') as MockSerialService:
            self.mock_serial_service = MockSerialService()
            from server import app
            app.config["TESTING"] = True
            app.config["DEBUG"] = True
            self.app = app.test_client()

    def test_get_status(self):
        self.mock_serial_service.read_line = mock.Mock(return_value=b"""{
        "tidalVolume" : "500",
        "respiratoryRate" : "25",
        "peakInspiratoryPressure" : "70",
        "ieRatio": "1:3",
        "peep": "7"
    }""")
        response = self.app.get('/api/ventilator', follow_redirects=True)
        self.mock_serial_service.send_message.assert_called_with(b"getStats\n")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'{\n  "ieRatio": "1:3", \n  "peakInspiratoryPressure": "70", \n  "peep": "7", '
                         b'\n  "respiratoryRate": "25", \n  "tidalVolume": "500"\n}\n', response.data)
