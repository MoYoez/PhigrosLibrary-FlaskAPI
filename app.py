import json

from flask import Flask, jsonify, request, make_response
from method import BestsRender

app = Flask(__name__)
# init

BestsRender.read_difficulty("difficulty.csv")
BestsRender.read_playerInfo("info.csv")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World! Phigros API SERVICE IS ALIVE!"})


@app.route("/api/phi/bests", methods=["GET"])
def get_bests():
    session = request.args.get("session")
    overflow = request.args.get("overflow")
    if session is None:
        return jsonify({"message": "session is required."})
    if overflow is None:
        overflow = 0
    else:
        overflow = int(overflow)
    try:
        bests, isphi = BestsRender.get_bests(session, overflow)
        is_phi = {"phi": isphi}
        best_list_args = {"bests": bests}
        best_list = {**is_phi, **best_list_args}
        get_formatData = BestsRender.get_formatData(session)
        status = True
        content = {**best_list, **get_formatData}
        data = {"status": status, "content": content}
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        data = make_response(data)
        data.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception as e:
        return jsonify({"message": str(e)})
    return data


if __name__ == "__main__":
    app.run(debug=True)
