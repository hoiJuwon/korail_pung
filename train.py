import requests
from bs4 import BeautifulSoup
import json
import io

city_path = {
    "서울특별시": 'https://m.map.naver.com/search2/search.nhn?query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "인천광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "대전광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "대구광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EB%8C%80%EC%A0%84%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "광주광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EA%B4%91%EC%A3%BC%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "울산광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EA%B4%91%EC%A3%BC%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "부산광역시": 'https://m.map.naver.com/search2/search.nhn?query=%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "세종특별자치시": 'https://m.map.naver.com/search2/search.nhn?query=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%1C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "경기도": 'https://m.map.naver.com/search2/search.nhn?query=%EC%84%B8%EC%A2%85%ED%8A%B9%EB%B3%84%EC%9E%90%EC%B9%98%EC%8B%9C%1C%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "강원도": 'https://m.map.naver.com/search2/search.nhn?query=%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "충청남도": 'https://m.map.naver.com/search2/search.nhn?query=%EA%B0%95%EC%9B%90%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "충청북도": 'https://m.map.naver.com/search2/search.nhn?query=%EC%B6%A9%EC%B2%AD%EB%82%A8%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "전라남도": 'https://m.map.naver.com/search2/search.nhn?query=%EC%B6%A9%EC%B2%AD%EB%B6%81%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "전라북도": 'https://m.map.naver.com/search2/search.nhn?query=%EC%A0%84%EB%9D%BC%EB%82%A8%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "경상남도": 'https://m.map.naver.com/search2/search.nhn?query=%EC%A0%84%EB%9D%BC%EB%B6%81%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
    "경상북도": 'https://m.map.naver.com/search2/search.nhn?query=%EA%B2%BD%EC%83%81%EB%82%A8%EB%8F%84%20%EA%B8%B0%EC%B0%A8%EC%97%AD&sm=hty&style=v5',
}

city_array = [
    "서울특별시",
    "인천광역시",
    "대전광역시",
    "대구광역시",
    "광주광역시",
    "울산광역시",
    "부산광역시",
    "세종특별자치시",
    "경기도",
    "강원도",
    "충청남도",
    "충청북도",
    "전라남도",
    "전라북도",
    "경상남도",
    "경상북도",
]
final_data = {
    "서울특별시": [],
    "인천광역시": [],
    "대전광역시": [],
    "대구광역시": [],
    "광주광역시": [],
    "울산광역시": [],
    "부산광역시": [],
    "세종특별자치시": [],
    "경기도": [],
    "강원도": [],
    "충청남도": [],
    "충청북도": [],
    "전라남도": [],
    "전라북도": [],
    "경상남도": [],
    "경상북도": [],
}


headers = {
    'authority': 'm.map.naver.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': '',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=EBMUAUGHMBDV4; _ga=GA1.2.675216546.1581935389; ASID=0e38461c000001708a6f291f0000004e; MM_NEW=1; NFS=2; NRTK=ag#20s_gr#3_ma#0_si#1_en#0_sp#0; nx_ssl=2; page_uid=UrXtKwp0JWVssuXcgfRssssste4-441781; _naver_usersession_=vHSeGV0xWtA4l3wsrQE/TFlC; JSESSIONID=4BCFA9CB42D6720F4D817FF66B93AAC3; BMR=s=1589349156304&r=https%3A%2F%2Fm.map.naver.com%2Fsearch2%2Fsearch.nhn%3Fquery%3D%25EB%25B6%2580%25EC%2582%25B0%25EC%258B%259C%2520%25EA%25B8%25B0%25EC%25B0%25A8%25EC%2597%25AD%26sm%3Dhty%26style%3Dv5&r2=https%3A%2F%2Fm.map.naver.com%2Fsearch2%2Fsearch.nhn%3Fquery%3D%25EC%2584%259C%25EC%259A%25B8%25ED%258A%25B9%25EB%25B3%2584%25EC%258B%259C%2520%25EA%25B8%25B0%25EC%25B0%25A8%25EC%2597%25AD%26sm%3Dhty%26style%3Dv5',
}

for i in city_array:
    headers['referer'] = city_path[i]

    params = (
        ('query', i + '기차역'),
        ('sm', 'clk'),
        ('style', 'v5'),
        ('page', '1'),
        ('displayCount', '75'),
        ('type', 'SITE_1'),
    )

    response = requests.get(
        'https://m.map.naver.com/search2/searchMore.nhn', headers=headers, params=params)

    # print(type(response.text))

    result_list = json.loads(response.text)['result']['site']['list']

    for l in result_list:
        print(l['name'])
        final_data_schema = {
            'name': '',
            'category': '',
            'address': ''
        }
        final_data_schema['name'] = l['name']
        final_data_schema['category'] = l['category']
        final_data_schema['address'] = l['address']

        final_data[i].append(final_data_schema)

    # print(json.loads(response.text)['result']['site']['list'])
    # employees_obj = json.loads(json_string)

with io.open('train_data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(final_data, ensure_ascii=False))
