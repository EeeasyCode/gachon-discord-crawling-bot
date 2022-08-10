import json
import requests
import xmltodict


def subway(way):
    hh_url = 'http://swopenapi.seoul.go.kr/api/subway/sample/xml/realtimeStationArrival/0/5/가천대'

    html = requests.get(hh_url).text
    dic = xmltodict.parse(html)
    jsonString = json.dumps(dic['realtimeStationArrival']['row'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    if way == '복정':
        return jsonObj[0], jsonObj[1]
    elif way == '태평':
        return jsonObj[2], jsonObj[3]
    else:
        return "방면을 제대로 입력해주세요."

