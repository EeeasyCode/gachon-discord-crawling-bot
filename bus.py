import config
import json
import requests
import xmltodict


def gachon_bus(busNo):
    url = "https://api.odsay.com/v1/api/searchStation"
    params = {'apiKey': 'd2GBfNZwQNO2MR9wddUChJih4a11WiaSHf8WATyp9R8', 'lang': 0, 'stationName': '가천대', 'CID': '1010'}

    response = requests.get(url, params=params)
    response_dic = eval(response.text)
    localStationID = response_dic['result']['station'][0]['localStationID']
    gachon_uni_Bus_Info = {
        "1312": ["241006200", "천안 | 동서울터미널 <-> 아산시외버스터미널"],
        "1309": ["241006190", "천안 | 동서울터미널 <-> 천안총합터미널"],
        "3000": ["227000038", "하남 | 미사강변호반써밋 <-> 금토천교"],
        "8401": ["234001426", "의정부 | 낙양동공영차고지 <-> 수원역.노보텔수원"],
        "1650": ["234000050", "구리 | 구리수택차고지 <-> 안양역"],
        "1112": ["234000016", "창현마을.수원신갈IC 방면", "수원 | 경희대차고지 <-> 테크노마트앞.강변역(C)"],
        "8109": "234001236",
        "8409": "234001246",
        "1801": "241000830",
        "8147": "241000820",
        "8153": "241000840",
        "G2100": "230000179",
        "G6009": "233000322",
    }

    for i in gachon_uni_Bus_Info:
        if i == busNo:
            busLocalBlID = gachon_uni_Bus_Info[i][0]
            busLocation = gachon_uni_Bus_Info[i][1]
            busEndStart = gachon_uni_Bus_Info[i][2]
            break

    gc_bus_url = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList"
    gc_bus_params = {
        'serviceKey': config.BUS_CONFIG['service-key'],
        'stationId': localStationID
    }
    gc_bus_response = requests.get(gc_bus_url, params=gc_bus_params)
    gc_bus_dict = xmltodict.parse(gc_bus_response.text)
    for i in range(len(gc_bus_dict['response']['msgBody']['busArrivalList'])):
        if gc_bus_dict['response']['msgBody']['busArrivalList'][i]['routeId'] == busLocalBlID:
            busKey = gc_bus_dict['response']['msgBody']['busArrivalList'][i]
            localtionNo1 = json.loads(json.dumps(busKey['locationNo1'], ensure_ascii=False))
            localtionNo2 = json.loads(json.dumps(busKey['locationNo2'], ensure_ascii=False))
            predictTime1 = json.loads(json.dumps(busKey['predictTime1'], ensure_ascii=False))
            predictTime2 = json.loads(json.dumps(busKey['predictTime2'], ensure_ascii=False))
            remainSeatCnt1 = json.loads(json.dumps(busKey['remainSeatCnt1'], ensure_ascii=False))
            remainSeatCnt2 = json.loads(json.dumps(busKey['remainSeatCnt2'], ensure_ascii=False))
            return busNo, busLocation, busEndStart, localtionNo1, localtionNo2, predictTime1, predictTime2, remainSeatCnt1, remainSeatCnt2
