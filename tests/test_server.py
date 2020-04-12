from unittest import TestCase, mock


class TestGetStatus(TestCase):
    @mock.patch('serial_connection.SerialConnection', autospec=True)
    def setUp(self, mock_serial_connection) -> None:
        from server import VentilatorStatus
        self.get_status = VentilatorStatus(**{'serial_connection': mock_serial_connection})
        self.mock_serial_connection = mock_serial_connection

    def test_get_status(self):
        self.mock_serial_connection.configure_mock(**{'request.return_value': b'{}'})
        response = self.get_status.get()
        self.mock_serial_connection.request.assert_called_with("getStats\n")
        self.assertEqual(response, {})
