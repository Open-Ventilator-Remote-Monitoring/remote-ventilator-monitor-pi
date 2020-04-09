from unittest import TestCase, mock


class Test(TestCase):
    @mock.patch('serial_connection_factory.SerialConnectionFactory', autospec=True)
    @mock.patch('serial_connection.SerialConnection', autospec=True)
    def setUp(self, mock_serial_connection, mock_serial_connection_factory) -> None:
        mock_serial_connection_factory.configure_mock(**{'create_serial_connection.return_value': mock_serial_connection})
        self.mock_serial_connection = mock_serial_connection
        from server import app
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    def test_get_status(self):
        self.mock_serial_connection.configure_mock(**{
            'read_line.return_value': b'{"tidalVolume":"500","respiratoryRate":"25","peakInspiratoryPressure"'
                                      b' : "70","ieRatio": "1:3","peep": "7"}'})
        response = self.app.get('/api/ventilator', follow_redirects=True)
        self.mock_serial_connection.send_message.assert_called_with(b"getStats\n")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'{\n  "ieRatio": "1:3", \n  "peakInspiratoryPressure": "70", \n  "peep": "7", '
                         b'\n  "respiratoryRate": "25", \n  "tidalVolume": "500"\n}\n', response.data)
