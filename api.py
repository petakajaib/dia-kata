from flask import Flask, jsonify
from random import random

api = Flask(__name__)

d = {"bo": "la"}

@api.route("/search/")
def search():
    return jsonify(**d)

@api.route("/detail/")
def detail():
    d[str(random())] = random()
    return jsonify(**d)

@api.route("/top_people/")
def top_people():
    return jsonify(top_people=["person1", "person2", "person3"])

@api.route("/fasttext/")
def load_models():
    return jsonify(ja=['pa'])

@api.route("/annoy/")
def load_models():
    return jsonify(ja=['pa'])
