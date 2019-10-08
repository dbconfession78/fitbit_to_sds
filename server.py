from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
CORS(app)

class OCS_Type(Resource):
    def get(self):
        return {'type': 'done'}

api.add_resource(OCS_Type, '/create_type')

if __name__ == '__main__':
    app.run(port=5000)
