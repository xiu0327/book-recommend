from flask import Flask, request
from func import print_json, userLoanlist
from flask_cors import CORS
from flask_restx import Api, Resource
from lists import List

app = Flask(__name__)
api = Api(
    app,
    title="Book치기 박치기 API Server",
    contact="codinging0326@gmail.com"
)

CORS(app, resources={r'*': {'origins': '*'}})
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})

api.add_namespace(List, '/lists')
