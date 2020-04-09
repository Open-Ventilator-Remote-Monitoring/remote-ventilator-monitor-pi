
from flask import Flask, jsonify
from flask_cors import CORS
import yaml
from yaml import Loader

from serial_connection_factory import SerialConnectionFactory

app = Flask(__name__)
CORS(app)


@app.before_first_request
def init():
    config_file = "application-{}.yml".format(app.config["ENV"])
    try:
        with open(config_file) as file:
            config = yaml.load(file, Loader=Loader)
            print(config)
            print(f'Config loaded from {config_file}')
    except OSError:
        print(f'Warning, could not load configuration {config_file}')

    global serial_connection
    serial_connection = SerialConnectionFactory.create_serial_connection(config['ventilator']['connection'])
    serial_connection.start_connection()


@app.route("/")
def hello():
    return_string = "<h1>Ventilator Network Server</h1>"
    return_string += "<p>Ventilator Stats:</p>"
    return return_string


@app.route("/api/ventilator", methods=['GET'])
def get_status():
    global serial_connection
    data = serial_connection.read_line()
    return jsonify({'ventilator': [data.__dict__]})

