import json

from flask import Flask, jsonify, request, make_response
from method import (
    BestsRender,
    difficulty,
    info,
    info_by,
    levels,
    song_info_handler_main,
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
    songinfo = request.args.get("songinfo")
    if session is None:
        return jsonify({"message": "session is required."})
    if overflow is None:
        overflow = 0
    else:
        overflow = int(overflow)
    if songinfo is None or songinfo == "false":
        songinfo = False
    else:
        songinfo = True
    try:
        bests, isphi = BestsRender.get_bests(session, overflow)
        is_phi = {"phi": isphi}
        best_list_args = {"bests": bests}
        best_list = {**is_phi, **best_list_args}
        get_formatData = BestsRender.get_formatData(session)
        content = {**best_list, **get_formatData}
        if songinfo:
            # generated a songslist id.
            i = 0
            songinfoList = []
            for _ in bests:
                listChatNum = bests[i]
                getSortSongID = listChatNum["songId"]
                songinfoList.append(song_info_handler_main(songid=getSortSongID))
                i = i + 1
            full_reply = {"songinfo": songinfoList}
            content = {
                **best_list,
                **full_reply,
                **get_formatData,
            }
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
    songinfo = request.args.get("songinfo")
    if session is None:
        return jsonify({"message": "session is required."})
    if songs is None:
        return jsonify({"message": "songid is required."})
    if diff is None:
        diff = "IN"
    if songinfo is None or songinfo == "false":
        songinfo = False
    else:
        songinfo = True
    try:
        Contents, msg = BestsRender.get_songs_stats(session, songs, diff)
        if Contents is None:
            data = {"status": False, "message": msg}
        else:
            get_formatData = BestsRender.get_formatData(session)
            Contents = {"record": Contents}
            Content = {**Contents, **get_formatData}
            if songinfo:
                dict_songinfo = {"song_info": song_info_handler_main(songid=songs)}
                Content = {**Content, **dict_songinfo}
            data = {"status": True, "content": Content}
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        data = make_response(data)
        data.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    return data


@app.route("/api/phi/rand", methods=["GET"])
def get_rand():
    songinfo = request.args.get("songinfo")
    if songinfo is None or songinfo == "false":
        songinfo = False
    else:
        songinfo = True
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
        if songinfo:
            dict_songinfo = {"song_info": song_info_handler_main(songid=result[0])}
            Content = {**Content, **dict_songinfo}
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
        data = {"status": True, "content": song_info_handler_main(songid=songid)}
    except Exception as e:
        return jsonify({"status": False, "message": str(e)})
    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    data = make_response(data)
    data.headers["Content-Type"] = "application/json; charset=utf-8"
    return data


if __name__ == "__main__":
    app.run(debug=True)
