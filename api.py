from flask import Flask, jsonify
api = Flask(__name__)

@api.route("/search/")
def search():
    return jsonify(results=["person1", "person2"])

@api.route("/detail/")
def detail():
    return jsonify(name="Person 1")

@api.route("/top_people/")
def top_people():
    return jsonify(top_people=["person1", "person2", "person3"])
