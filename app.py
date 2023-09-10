from flask import Flask, request, jsonify
from flights import number_of_new_connections
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/airport-connections', methods=["POST"])
def airport_connections():
    result = {}
    data = request.get_json()
    try:
        result = number_of_new_connections(data['starting_connection'], data['airport_codes'], data['connections'])
    except Exception as e:
        data['error'] = e

    return jsonify(result), 201


if __name__ == '__main__':
    app.run()
