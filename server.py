from flask import Flask, jsonify
from flask_cors import CORS
import serial
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

# ser=serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser.flush()


ventilator = [
    {
        'tidalVolume' : u'500',
        'respiratoryRate' : u'25',
        'peakInspiratoryPressure' : u'70',
        'ieRatio' : u'1:3',
        'peep' : u'7'
    }
]

@app.route("/")
def hello():
    return_string = "<h1>Ventilator Network Server</h1>"
    return_string += "<p>Ventilator Stats:</p>"
    return return_string

@app.route("/api/ventilator", methods=['GET'])
def get_status():

    return jsonify({'ventilator': ventilator})
    # ser.write(b"getStats\n")
    # line = ser.readline().decode('utf-8').rstrip()
    # jsonline = json.loads(line)
    # print(line)
    # print(jsonline)
    # return(jsonline)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
