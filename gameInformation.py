from UnityPy import Environment
from tqdm import tqdm

import os
import zipfile
import requests

import struct
import sys

# download gameinformation from


filename = sys.argv[1].split("/")[-1]


class ByteReader:
    def __init__(self, data: bytes):
        self.data = data
        self.position = 0
        self.d = {int: self.readInt, float: self.readFloat, str: self.readString}

    def readInt(self):
        self.position += 4
        return self.data[self.position - 4] ^ self.data[self.position - 3] << 8

    def readFloat(self):
        self.position += 4
        return struct.unpack("f", self.data[self.position - 4 : self.position])[0]

    def readString(self):
        length = self.readInt()
        result = self.data[self.position : self.position + length].decode()
        self.position += length // 4 * 4
        if length % 4 != 0:
            self.position += 4
        return result

    def skipString(self):
        length = self.readInt()
        self.position += length // 4 * 4
        if length % 4 != 0:
            self.position += 4

    def readSchema(self, schema: dict):
        result = []
        for x in range(self.readInt()):
            item = {}
            for key, value in schema.items():
                if value in (int, str, float):
                    item[key] = self.d[value]()
                elif type(value) == list:
                    l = []
                    for i in range(self.readInt()):
                        l.append(self.d[value[0]]())
                    item[key] = l
                elif type(value) == tuple:
                    for t in value:
                        self.d[t]()
                elif type(value) == dict:
                    item[key] = self.readSchema(value)
                else:
                    raise Exception("无")
            result.append(item)
        return result


def run(path):
    env = Environment()
    with zipfile.ZipFile(path) as apk:
        with apk.open("assets/bin/Data/globalgamemanagers.assets") as f:
            env.load_file(f.read(), name="assets/bin/Data/globalgamemanagers.assets")
        with apk.open("assets/bin/Data/level0") as f:
            env.load_file(f.read())
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        data = obj.read()
        if data.m_Script.get_obj().read().name == "GameInformation":
            information = data.raw_data.tobytes()

    position = information.index(b"\x16\x00\x00\x00Glaciaxion.SunsetRay.0\x00\x00\n")

    reader = ByteReader(information[position - 4 :])
    information_schema = {
        "songId": str,
        "songKey": str,
        "songName": str,
        "songTitle": str,
        "difficulty": [float],
        "illustrator": str,
        "charter": [str],
        "composer": str,
        "levels": [str],
        "previewTime": float,
        "unlockList": {"unlockType": int, "unlockInfo": [str]},
        "n": [int],
    }
    difficulty = []
    table = []
    for i in range(3):
        for item in reader.readSchema(information_schema):
            item["songId"] = item["songId"][:-2]
            if len(item["levels"]) == 5:
                item["difficulty"].pop()
                item["charter"].pop()
            if item["difficulty"][-1] == 0:
                item["difficulty"].pop()
                item["charter"].pop()
            for i in range(len(item["difficulty"])):
                item["difficulty"][i] = round(item["difficulty"][i], 1)
            difficulty.append([item["songId"]] + item["difficulty"])
            table.append(
                (
                    item["songId"],
                    item["songName"],
                    item["composer"],
                    item["illustrator"],
                    *item["charter"],
                )
            )

    print(difficulty)
    print(table)

    with open("difficulty.csv", "w", encoding="utf8") as f:
        for item in difficulty:
            f.write(",".join(map(str, item)))
            f.write("\n")

    with open("info.csv", "w", encoding="utf8") as f:
        for item in table:
            f.write("\\".join(item))
            f.write("\n")


if __name__ == "__main__":
    response = requests.get(sys.argv[1], stream=True)
# get length.
total = int(response.headers.get("content-length", 0))


with open(filename, "wb") as file, tqdm(
    desc=filename,
    total=total,
    unit="iB",
    unit_scale=True,
    unit_divisor=1024,
) as bar:
    for data in response.iter_content(chunk_size=1024):
        size = file.write(data)
        bar.update(size)


run(filename)
os.remove(filename)
