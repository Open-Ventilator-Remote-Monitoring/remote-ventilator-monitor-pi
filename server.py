from flask import Flask
from flask_cors import CORS
import json

from serial_connection_factory import SerialConnectionFactory

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

serial_connection = SerialConnectionFactory.create_serial_connection(link='/dev/ttyACM0', baud=9600, timeout=1)
serial_connection.start_connection()

""" `
ventilator = [
    {
        'tidalVolume' : u'500',
        'respiratoryRate' : u'25',
        'peakInspiratoryPressure' : u'70',
        'ieRatio' : u'1:3',
        'peep' : u'7'
    }
]
"""


@app.route("/")
def hello():
    return_string = "<h1>Ventilator Network Server</h1>"
    return_string += "<p>Ventilator Stats:</p>"
    return return_string


@app.route("/api/ventilator", methods=['GET'])
def get_status():
    # return jsonify({'ventilator': ventilator})
    serial_connection.send_message(b"getStats\n")
    line = serial_connection.read_line().decode('utf-8').rstrip()
    json_line = json.loads(line)
    print(line)
    print(json_line)
    return json_line


if __name__ == "__main__":
    app.run(host='0.0.0.0')
