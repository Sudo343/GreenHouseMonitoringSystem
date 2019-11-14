#!venv-flask/bin/python
#!venv-flask/bin/flask
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

evaluationResult =  { "details" : "Pepper__bell_Bacterial_spot" }

@app.route('/')
def index():
    return "Welcome to Green House Monitoring System. Pass data as payload to evaluate results"

@app.route('/evaluate', methods=['POST'])
def evaluateResult():
    if not request.json or not 'payload' in request.json:
        abort(400)
    return jsonify(evaluationResult), 201

@app.errorhandler(400)
def payloadNotPassed(error):
    return make_response(jsonify({'error': 'Please pass base64 encoded image data in key payload'}), 400)

@app.errorhandler(405)
def methodNotAllowed(error):
    return make_response(jsonify({'error': 'Please do a post call to this api with payload'}), 405)

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Please do a POST call with payload in order to get evaluation results'}), 404)

@app.errorhandler(500)
def internalServerError(error):
    return make_response(jsonify({'error': ('Something went wrong with server' + error)}), 500)

if __name__ == '__main__':
    app.run(debug=True)