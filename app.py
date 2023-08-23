import json

from flask import Flask, jsonify, request, make_response
from method import (
    BestsRender,
    difficulty,
    info,
    info_by,
    levels,
    info_illustrator,
    info_hd_designer,
    info_at_designer,
    info_ez_desinger,
    info_in_desingner,
)
import random as rand


app = Flask(__name__)
# init

BestsRender.read_difficulty("difficulty.csv")
BestsRender.read_playerInfo("info.csv")
listDiff = list(difficulty.items())
getLength = len(difficulty)


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
        content = {**best_list, **get_formatData}
        data = {"status": True, "content": content}
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        data = make_response(data)
        data.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    return data


@app.route("/api/phi/best", methods=["GET"])
def get_songs():
    session = request.args.get("session")
    songs = request.args.get("songid")
    diff = request.args.get("diff")
    if session is None:
        return jsonify({"message": "session is required."})
    if songs is None:
        return jsonify({"message": "songid is required."})
    if diff is None:
        diff = "IN"
    try:
        Contents, msg = BestsRender.get_songs_stats(session, songs, diff)
        if Contents is None:
            data = {"status": False, "message": msg}
        else:
            get_formatData = BestsRender.get_formatData(session)
            Contents = {"record": Contents}
            Content = {**Contents, **get_formatData}
            data = {
                "status": True,
                "content": Content,
            }
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        data = make_response(data)
        data.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    return data


@app.route("/api/phi/rand", methods=["GET"])
def get_rand():
    try:
        getRandSongIDNum = rand.randrange(0, getLength)
        result = listDiff[getRandSongIDNum - 1]
        result_info_name = info[result[0]]
        result_info_by = info_by[result[0]]
        result_get_diff_list = result[1]
        getLength_result_range = rand.randrange(0, len(result_get_diff_list))
        getLevel = levels[getLength_result_range]
        getRating = result_get_diff_list[getLength_result_range]
        Content = {
            "songid": result[0],
            "songname": result_info_name,
            "composer": result_info_by,
            "level": getLevel,
            "rating": getRating,
        }
        data = {
            "status": True,
            "content": Content,
        }
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        data = make_response(data)
        data.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    return data


@app.route("/api/phi/info", methods=["GET"])
def get_info():
    session = request.args.get("session")
    if session is None:
        return jsonify({"message": "session is required."})
    try:
        get_formatData = BestsRender.get_formatData(session)
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    data = {"status": True, "Content": get_formatData}
    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    data = make_response(data)
    data.headers["Content-Type"] = "application/json; charset=utf-8"
    return data


@app.route("/api/phi/song", methods=["GET"])
def get_song_info():
    songid = request.args.get("songid")
    if songid is None:
        return jsonify({"message": "songid is required."})
    try:
        result_info_name = info[songid]
        result_info_by = info_by[songid]
        result_get_diff_list: list = difficulty[songid]  # list
        result_get_ins_by = info_illustrator[songid]
        result_get_ez_designer = info_ez_desinger[songid]
        result_get_hd_desinger = info_hd_designer[songid]
        result_get_in_desinger = info_in_desingner[songid]
        result_get_at_desinger = info_at_designer[songid]
        showEZDetailed = {
            "EZ": {"rating": result_get_diff_list[0], "charter": result_get_ez_designer}
        }
        showHDDetailed = {
            "HD": {"rating": result_get_diff_list[1], "charter": result_get_hd_desinger}
        }
        showInDetailed = {
            "In": {"rating": result_get_diff_list[2], "charter": result_get_in_desinger}
        }
        if len(result_get_diff_list) >= 4:
            showAtDetailed = {
                "In": {
                    "rating": result_get_diff_list[3],
                    "charter": result_get_at_desinger,
                }
            }
        else:
            showAtDetailed = {}
        getChartDetailedInfo = {
            **showEZDetailed,
            **showHDDetailed,
            **showInDetailed,
            **showAtDetailed,
            "level_list": result_get_diff_list,
        }
        infos = {
            "songname": result_info_name,
            "composer": result_info_by,
            "illustrator": result_get_ins_by,
            "chartDetail": getChartDetailedInfo,
        }
        content = {"songid": songid, "info": infos}
        data = {"status": True, "content": content}
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    data = make_response(data)
    data.headers["Content-Type"] = "application/json; charset=utf-8"
    return data


if __name__ == "__main__":
    app.run(debug=True)
