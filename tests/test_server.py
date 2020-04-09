from unittest import TestCase, mock
import server

class Test(TestCase):
    @mock.patch('serial_connection.SerialConnection', autospec=True)
    def setUp(self, mock_serial_connection) -> None:
        self.mock_serial_connection = mock_serial_connection
        server.serial_connection = mock_serial_connection
        server.app.config["TESTING"] = True
        server.app.config["DEBUG"] = True
        self.app = server.app.test_client()

    def test_get_status(self):
        self.mock_serial_connection.configure_mock(**{
            'request.return_value': b'{"tidalVolume":"500","respiratoryRate":"25","peakInspiratoryPressure"'
                                      b' : "70","ieRatio": "1:3","peep": "7"}'})
        response = self.app.get('/api/ventilator', follow_redirects=True)
        self.mock_serial_connection.request.assert_called_with("getStats\n")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'{\n  "ieRatio": "1:3", \n  "peakInspiratoryPressure": "70", \n  "peep": "7", '
                         b'\n  "respiratoryRate": "25", \n  "tidalVolume": "500"\n}\n', response.data)
