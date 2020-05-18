from bs4 import BeautifulSoup
import requests
import json
import io


cookies = {
    'JSESSIONID': 'nFSYNeN23pq6wKgsq19HLWyjHAnBKDNCh2bfaJEgMZng7XDO4aVlzUHcnlefI5ea',
    'WMONID': 'Z1EZwxZ-fwt',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://www.letskorail.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do',
    # 'Referer': 'http://www.letskorail.com/ebizprd/prdMain.do',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}


# start_city = input('ex ) 서울 \n')
# end_city = input('ex ) 부산\n')
# start_time = input('출발 시간 : ex)16\n')
# start_month = input('ex ) 05\n')
# start_day = input('ex ) 14 \n')

# # 테스트용
# start_city = '서울'
# end_city = '부산'
# # start_time = '20'
# start_month = '05'
# start_day = '23'

# input 용
print('************************************')
print('출발지 / 도착지 / 월 / 요일 입력하면 전부 가져옵니다.')

start_city = input('ex ) 서울 \n')
end_city = input('ex ) 부산\n')
start_month = input('ex ) 05\n')
start_day = input('ex ) 14 \n')


final_data = []


def get_korail_data(start_time):

    data = {
        'txtGoStartCode': '',
        'txtGoEndCode': '',
        'radJobId': '1',
        'selGoTrain': '05',
        'txtSeatAttCd_4': '015',
        'txtSeatAttCd_3': '000',
        'txtSeatAttCd_2': '000',
        'txtPsgFlg_2': '0',
        'txtPsgFlg_3': '0',
        'txtPsgFlg_4': '0',
        'txtPsgFlg_5': '0',
        'chkCpn': 'N',
        'selGoSeat1': '015',
        'selGoSeat2': '',
        'txtPsgCnt1': '1',
        'txtPsgCnt2': '0',
        'txtGoPage': '1',
        'txtGoAbrdDt': '2020' + start_month+start_day,
        'selGoRoom': '',
        'useSeatFlg': '',
        'useServiceFlg': '',
        'checkStnNm': 'Y',
        'txtMenuId': '11',
        'SeandYo': 'N',
        'txtGoStartCode2': '',
        'txtGoEndCode2': '',
        'hidEasyTalk': '',
        'txtGoStart': start_city,
        'txtGoEnd': end_city,
        'start': '2020.' + start_month + '.' + start_day,
        'selGoHour': start_time,
        # 'txtGoHour': '142100',
        'txtGoHour': start_time + '0000',
        'selGoYear': '2020',
        'selGoMonth': start_month,
        'selGoDay': start_day,
        'txtGoYoil': '\uBAA9',
        'txtPsgFlg_1': '1'
    }

    response = requests.post('http://www.letskorail.com/ebizprd/EbizPrdTicketPr21111_i1.do',
                             headers=headers, cookies=cookies, data=data, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.select(
        '#container > #contents > div > form > #center > #divResult > #tableResult')

    # print(str(container[0]).find('tr class'))
    # print(container[0].find_all('tr'))
    if container is not None:
        if len(container) is not 0:
            tr_container = container[0].find_all('tr')
        else:
            return 0

    # 구분 / 열차번호 / 출발 / 도착 / 멤버쉽 혜택 / 소요시간

    count = 0
    for t in tr_container:

        # 첫번째 로우 점프
        if count == 0:
            count += 1

            continue

        final_data_schema = {
            "type":  '',
            "train_num": '',
            "dep_time": '',
            "arr_time": '',
            "price": '',
            "tot_time": '',
            "membership": ''
        }

        # print(t.text.replace(' ', '').split())
        target_array = t.text.split()
        # print(target_array)

        # final_data_schema['type'] = target_array[0]

        print(target_array)
        print('뭔데')
        # ktx
        if target_array[1] == 'KTX':
            ktx_train_num = target_array.pop(2)
            target_array[1] = target_array[1]+' '+ktx_train_num

            if '할인' in target_array[6]:
                # print(target_array)
                percent = target_array.pop(5) + ' ' + target_array[5][:2]
                # print(percent)
                target_array[5] = target_array[5][2:-1]
                target_array.append(percent)
                # print('여기임')
                # print(target_array)
                if len(target_array) == 10:
                    target_array.pop(-3)
                    target_array.pop(-3)
                elif len(target_array) == 9:
                    target_array.pop(-3)

            elif '적립' in target_array[6]:
                # print(target_array)
                target_array.pop(6)
                # target_array[5] = target_array[5] + add
                add = target_array[5][target_array[5].find(
                    '%')-1: target_array[5].find('%')+1] + ' ' + '적립'
                target_array[5] = target_array[5][:target_array[5].index('원')]
                target_array.append(add)
                if len(target_array) == 7 or len(target_array) == 10:
                    target_array.pop(-3)
                    target_array.pop(-3)
                elif len(target_array) == 6 or len(target_array) == 9:
                    target_array.pop(-3)

            # print(target_array)
            # final_data_schema['train_num'] = target_array[1]
            # final_data_schema['depart_time'] = target_array[3][2:]
            # final_data_schema['arrive_time'] = target_array[3][2:]
            # # if
            # # final_data_schema['price'] = target_array[6][:target_array[6].index(
            # #     '원')]
            # final_data_schema['membership'] = target_array[7][target_array[7].find(
            #     '%')-1: target_array[7].find('%')+1]
            # final_data_schema['time'] = target_array[-1]
            # # print(target_array[-1])
            # final_data.append(final_data_schema)
            # 나머지
            target_array.pop(4)

        else:
            if len(target_array) == 9:
                target_array.pop(-2)
                target_array.pop(-2)
            else:
                target_array.pop(5)
                target_array.pop(4)
                target_array.pop(-2)
                target_array.pop(-2)
            # print('시발버야')
            # print(target_array)
            target_array[-2] = target_array[-2][:target_array[-2].find('원')]
            target_array.append('none')
            if len(target_array) == 8:
                target_array.pop(4)
            else:
                pass

        print(target_array)

        # target_array.pop(6)

        # print('나머지임')

        # print(target_array[5])
        if len(target_array) is not 7:
            error_cities = start_city + ' ' + end_city

            with io.open('에러.txt', 'w', encoding='utf-8') as f:
                f.write((error_cities, ensure_ascii=False))

            continue

        else:
            final_data_schema['type'] = target_array[0]
            final_data_schema['train_num'] = target_array[1]
            final_data_schema['dep_time'] = target_array[2]
            final_data_schema['arr_time'] = target_array[3]
            final_data_schema['price'] = target_array[4]
            final_data_schema['tot_time'] = target_array[5]
            final_data_schema['membership'] = target_array[6]

            final_data.append(final_data_schema)

        # if '-' in t.text.split():

        # final_data_schema['type'] = t.contents[0]


ct = 1

for t in range(24):
    print('돌고 있습니다 ' + ct*'*')
    ct += 1
    get_korail_data(str(t))

for i in final_data:
    print('구분 : ', i['type'])
    print('열차 : ', i['train_num'])
    print('출발시간 : ', i['dep_time'])
    print('도착시간 : ', i['arr_time'])
    print('가격 : ', i['price'])
    print('소요 시간 : ', i['tot_time'])
    print('혜택 : ', i['membership'])
    print('------------------------------')


with io.open(f'{start_city}_{end_city}_{start_month}월{start_day}.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(final_data, ensure_ascii=False))


# 예외처리해야됨
# 23일
