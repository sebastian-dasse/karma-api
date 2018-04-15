#!/usr/bin/env python

"""
TODO: comment

inspired by:
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

--> CONTINUE READING AT:
Improving the web service interface


--> FOR FURTHER IMPROVEMENTS HAVE A LOOK AT:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

defines the following routes:

GET    /yogis
GET    /yogis/<yid>
POST   /yogis
PUT    /yogis/<yid>
DELETE /yogis/<yid>
"""

from flask import Flask, jsonify, abort, make_response, request


app = Flask(__name__)

server_ip = "0.0.0.0"
server_port = 5000


base_url = "/karma/api/v1"

yogis = {
  "Alice": 0,
  "Carla": 0,
  "Bob": 0
}
default_karma = 0


@app.route("/")
def index():
  return (
    "<h1>Welcome to the Karma API!</h1>"
    "<p>You can query or update the yogis at <code>" + base_url + "/yogis</code></p>"
  )


@app.route(base_url + "/yogis", methods=["GET"])
def get_yogis():
  return jsonify({"yogis": yogis})


@app.route(base_url + "/yogis/<yid>", methods=["GET"])
def get_karma(yid):
  if not yid in yogis:
    abort(404)
  return jsonify({yid: yogis[yid]})


@app.route(base_url + "/yogis", methods=["POST"])
def create_yogi():
  if (not request.json or
      not "yid" in request.json or 
      request.json["yid"] in yogis):
    abort(400)
  yid = request.json["yid"]
  karma = request.json.get("karma", default_karma)
  yogis[yid] = karma
  return jsonify({yid: karma}), 201


@app.route(base_url + "/yogis/<yid>", methods=["PUT"])
def update_karma(yid):
  if not yid in yogis:
    abort(404)
  if (not request.json or
      not "karma" in request.json or 
      type(request.json["karma"]) is not int):
    abort(400)
  yogis[yid] += request.json["karma"]
  return jsonify({yid: yogis[yid]})


@app.route(base_url + "/yogis<yid>", methods=["DELETE"])
def delete_yogi():
  if not yid in yogis:
    abort(404)
  yogis.pop(yid)
  return jsonify({"result": True})


@app.errorhandler(400)
def err_bad_request(error):
  return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(404)
def err_not_found(error):
  return make_response(jsonify({"error": "Not found"}), 404)


def main():
  import sys
  if len(sys.argv) > 1:
    server_port = int(sys.argv[1])

  app.run(host=server_ip, port=server_port, debug=True)


if __name__ == '__main__':
  main()
