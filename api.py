from flask import Flask, jsonify
api = Flask(__name__)

@api.route("/search/")
def search():
    return jsonify(results=["person1", "person2"])

@api.route("/detail/")
def detail():
    return jsonify(name="Person 1")

# @api.route("/")
