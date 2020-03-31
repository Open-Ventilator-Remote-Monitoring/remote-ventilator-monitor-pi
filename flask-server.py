from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
