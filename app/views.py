# -*- coding: UTF-8 -*-
from flask import *
from app import app
from nltk.corpus import wordnet as wn
import requests
import json
import re

headers = {
    'Content-Type': "application/json",
}


@app.route('/search', methods=["POST"])
def search():
    def search(str, part, radius):
        def apppend(_dict, key):
            if key in _dict:
                _dict[key] += 1
            else:
                _dict[key] = 1

        items = re.split('[\s+-]+', str)
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
        return [i[0] for i in sorted(_dict.items(), key = lambda x: x[1], reverse=True)]

    ans = {}
    def group(i, str):
        if i == len(chn_list):
            ans_list = search(str, part, radius)
            if ans_list != []:
                ans[str] = ans_list
            return
        for item in chn_list[i]:
            group(i+1, str+"+"+item)
            if synset == "no":
                break

    lang = request.form["lang"]
    origin_items = request.form["item"].strip()
    part = request.form["part"]
    radius = int(request.form["radius"])
    synset = request.form["synset"]

    if lang != app.config["LANGUAGES"]["中文"]:
        chn_list = []
        for item in re.split('[\s+-]+', origin_items):
            chn_item = []
            for ss in wn.synsets(item, lang=lang):
                chn_item.extend(ss.lemma_names(app.config["LANGUAGES"]["中文"]))
            chn_list.append(list(set(chn_item)))
        for item in chn_list[0]:
            group(1, item)
            if synset == "no":
                break
    else:
        ans[origin_items] = search(origin_items, part, radius)

    if ans != {}:
        return render_template("search.html", search=True, success=True, ans=ans, items=origin_items)
    else:
        return render_template("search.html", search=True, success=False, items=origin_items)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html", search=False)
