# -*- coding: UTF-8 -*-
SECRET_KEY = "I_LOVE_PYTHON_NMSL"

ELASTIC_HOST = "http://localhost:9200"
ELASTIC_INDEX = "sogou0016"
ELASTIC_INDEX_WITH_PART = "sogou0016.out"
ELASTIC_TYPE = "line"
ELASTIC_URL = "/".join((ELASTIC_HOST, ELASTIC_INDEX, ELASTIC_TYPE))
ELASTIC_URL_WITH_PART = "/".join((ELASTIC_HOST, ELASTIC_INDEX_WITH_PART, ELASTIC_TYPE))

LANGUAGES = {
    "中文": "cmn",
    "English": "eng", # 英语
    "shqiptar": "als", # 阿尔巴尼亚语
    "العربية": "arb", # 阿拉伯语
    "български": "bul", # 保加利亚语
    "Català": "cat", # 加泰罗尼亚语
    "dansk": "dan", # 丹麦语
    "Ελληνικά": "ell", # 希腊语
    "Euskal": "eus", # 巴斯克语
    "فارسی": "fas", # 波斯语
    "suomalainen": "fin", # 芬兰语
    "Le français": "fra", # 法语
    "עברית": "heb", # 希伯来语
    "हिन्दी": "ind", # 印度语
    "lingua italiana": "ita", # 意大利语
    "日本語": "jpn", # 日语
    "Nederlands": "nld", # 荷兰语
    "Norsk språk": "nno", # 挪威语
    "Polski": "pol", # 波兰语
    "Português": "por", # 葡萄牙语
    "Српски": "slv", # 塞尔维亚语
    "Espanol": "spa", # 西班牙语
    "svenska": "swe", # 瑞典语
    "ไทย": "tha" # 泰语
}
