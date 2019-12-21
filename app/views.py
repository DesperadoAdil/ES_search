# -*- coding: UTF-8 -*-
from flask import *
from app import app
import requests
import json
import re


@app.route('/search', methods=["POST"])
def search():
    def apppend(_dict, key):
        if key in _dict:
            _dict[key] += 1
        else:
            _dict[key] = 1

    items = re.split('[\s+-]+', request.form["item"].strip())
    part = request.form["part"]
    radius = int(request.form["radius"])

    headers = {
        'Content-Type': "application/json",
    }

    payload = {
    	"query": {
            "bool": {
                "must": [{"match": {"text": i}} for i in items]
            }
    	},
    	"size": 100
    }

    if part == "all":
        url = "/".join((app.config["ELASTIC_URL"], "_search"))
    else:
        url = "/".join((app.config["ELASTIC_URL_WITH_PART"], "_search"))

    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    lines = [i["_source"]["text"] for i in data["hits"]["hits"]]
    _list = []
    _dict = {}
    for line in lines:
        flag = True
        for _item in items:
            _i = line.find(_item)
            if _i == -1:
                flag = False
                break
        if not flag:
            continue

        for _item in items:
            if part == "all":
                item_part = _item
            else:
                item_part = _item + "/\w"

            i = 1
            while i <= radius:
                pattern_f = "\S+ " * i + item_part
                pattern_b = item_part + " \S+" * i

                for match in re.findall(pattern_f, line):
                    text = match[:match.find(" ")]
                    if part == "all":
                        apppend(_dict, text)
                    elif part == text[-2:]:
                        apppend(_dict, text[:-2])

                for match in re.findall(pattern_b, line):
                    text = match[match.rfind(" ")+1:]
                    if part == "all":
                        apppend(_dict, text)
                    elif part == text[-2:]:
                        apppend(_dict, text[:-2])
                i += 1

    _list = [i[0] for i in sorted(_dict.items(), key = lambda x: x[1], reverse=True)]
    if _list != []:
        return render_template("search.html", search=True, success=True, ans=_list, items=request.form)
    else:
        return render_template("search.html", search=True, success=False)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html", search=False)
