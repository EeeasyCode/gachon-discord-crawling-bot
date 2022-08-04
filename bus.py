import config
import json
import requests
import xmltodict


def gachon_bus(stationName):
    if stationName == '환승정류장':
        url = "https://api.odsay.com/v1/api/searchStation"
        params = {'apiKey': 'd2GBfNZwQNO2MR9wddUChJih4a11WiaSHf8WATyp9R8', 'lang': 0, 'stationName': '가천대',
                  'CID': '1010'}

        response = requests.get(url, params=params)
        response_dic = eval(response.text)
        localStationID = response_dic['result']['station'][0]['localStationID']
        gachon_uni_Bus_Info = {
            "1312": ["241006200", "천안TG.단대.천안대 방면", "천안 | 동서울터미널 <-> 아산시외버스터미널"],
            "1309": ["241006190", "천안TG.단대.천안대 방면", "천안 | 동서울터미널 <-> 천안총합터미널"],
            "3000": ["227000038", "성남시청전면 방면", "하남 | 미사강변호반써밋 <-> 금토천교"],
            "8401": ["234001426", "의왕청계영업소 방면", "의정부 | 낙양동공영차고지 <-> 수원역.노보텔수원"],
            "1650": ["234000050", "의왕청계영업소 방면", "구리 | 구리수택차고지 <-> 안양역"],
            "1112": ["234000016", "창현마을.수원신갈IC 방면", "수원 | 경희대차고지 <-> 테크노마트앞.강변역(C)"],
            "8109": ["234001236", "야탑역.종합버스터미널(전면) 방면", "성남 | 오리역 <-> 킨텍스제2전시장"],
            "8409": ["234001246", "의왕청계영업소 방면", "의정부 | 낙양동공영차고지 <-> 수원역.노보텔수원"],
            "1801": ["241000830", "인천터미널 방면", "광주 | 동서울터미널 <-> 인천터미널"],
            "8147": ["241000820", "의왕톨게이트 방면", "광주 | 동서울터미널 <-> 안산터미널"],
            "8153": ["241000840", "주은.풍림아파트 방면", "광주 | 동서울터미널 <-> 동아방송대"],
            "G2100": ["230000179", "도암IC 방면", "이천 | 이천역 <-> 잠실광역환승센터"],
            "G6009": ["233000322", "현대트랜시스 방면", "화성 | 호수자이파밀리에.아이원 <-> 잠실광역환승센터"]
        }

        busNo = ['1312', '1309', '3000', '8401', '1650', '1112', '8109', '8409', '1801', '8147', '8153', 'G2100', 'G6009']
        busLocalBlID = []
        busLocation = []
        busEndStart = []
        for i in gachon_uni_Bus_Info:
            busLocalBlID.append(gachon_uni_Bus_Info[i][0])
            busLocation.append([gachon_uni_Bus_Info[i][1]])
            busEndStart.append([gachon_uni_Bus_Info[i][2]])

        gc_bus_url = "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList"
        gc_bus_params = {
            'serviceKey': config.BUS_CONFIG['service-key'],
            'stationId': localStationID
        }
        gc_bus_response = requests.get(gc_bus_url, params=gc_bus_params)
        gc_bus_dict = xmltodict.parse(gc_bus_response.text)
        locationNo1 = []
        locationNo2 = []
        predictTime1 = []
        predictTime2 = []
        remainSeatCnt1 = []
        remainSeatCnt2 = []
        for i in range(len(gc_bus_dict['response']['msgBody']['busArrivalList'])):
            busKey = [gc_bus_dict['response']['msgBody']['busArrivalList'][i]]
            locationNo1.append(json.loads(json.dumps(busKey[0]['locationNo1'], ensure_ascii=False)))
            locationNo2.append(json.loads(json.dumps(busKey[0]['locationNo2'], ensure_ascii=False)))
            predictTime1.append(json.loads(json.dumps(busKey[0]['predictTime1'], ensure_ascii=False)))
            predictTime2.append(json.loads(json.dumps(busKey[0]['predictTime2'], ensure_ascii=False)))
            remainSeatCnt1.append(json.loads(json.dumps(busKey[0]['remainSeatCnt1'], ensure_ascii=False)))
            remainSeatCnt2.append(json.loads(json.dumps(busKey[0]['remainSeatCnt2'], ensure_ascii=False)))

        return busNo, busLocation, busEndStart, locationNo1, locationNo2, predictTime1, predictTime2, remainSeatCnt1, remainSeatCnt2
