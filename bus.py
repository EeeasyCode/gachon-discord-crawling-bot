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

    for i in range(len(response_dic['result']['station'][0]['businfo'])):
        if response_dic['result']['station'][0]['businfo'][i]['busNo'] == busNo:
            busLocalBlID = response_dic['result']['station'][0]['businfo'][i]['busLocalBlID']
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
            return busNo, localtionNo1, localtionNo2, predictTime1, predictTime2, remainSeatCnt1, remainSeatCnt2
