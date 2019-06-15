from flask import Flask, request
# from telegram import send_message
import pprint
import requests
import time
from decouple import config

app = Flask(__name__)

token = config('TOKEN')
api_url = f'https://api.telegram.org/bot{token}'


# select = ''


#   127.0.0.1/
@app.route("/")
def hello():
    return "Hello World!"


#   127.0.0.1/telegram
# @app.route('/telegram')
# def telegram2():
#     send_message('함수 전달 완료')
#     return '전송완료'
select = ''
crawling = ''


@app.route(f'/{token}', methods=['POST'])
def telegram():
    pprint.pprint(request.get_json())
    message = request.get_json().get('message')
    print(message)
    global select
    global crawling
    if message is not None:
        chat_id = message.get('from').get('id')  # 명시적으로 나타내기위해 get 사용 추천
        text = message.get('text')
        print(select)
        if text[0:2] == '버스':
            if text[-2:] == '시작':
                select = 'bus'

                msg = '''
                        승차 정류장을 선택하세요
                    1. 강남역나라빌딩앞
                    2. 수원버스터미널
                    3. 경기도 문화의전당
                '''
                requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            elif text[-2:] in ['정지', '중단', '중지', '그만']:
                select = ''
                msg = '버스 알림을 정지합니다'
                requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')

        elif select == 'bus' and text[0] == '1':
            msg = '3007번 14분전 7정거장 22석'
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            time.sleep(5)
            msg = '3007번 8분전 4정거장 15석'
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            time.sleep(5)
            msg = '3007번 3분전 2정거장 10석'
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            select = ''

        elif text[0:3] == '크롤링':
            if text[-2:] == '시작':
                select = 'crawling'
                msg = '''
                    크롤링할 사이트를 선택하세요
                    1. OKKY
                    2. devkorea
                    3. devpia
                '''
                requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            elif text[-2:] in ['정지', '중단', '중지', '그만']:
                select = ''
                msg = '크롤링을 정지합니다.'
                requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
        elif select == 'crawling' and text[0] == '1':
            msg = '크롤링할 단어를 입력하세요'
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
        elif select == 'crawling':
            crawling = text
            msg = f'{crawling}이 포함된 글이 올라오면 알려드릴게요!'
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            time.sleep(5)
            msg = '''KB-KISA 핀테크 해커톤 관심있으신분 있으실까요?
                    https://okky.kr/article/590299
                '''
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')
            time.sleep(5)
            msg = '''2019 서울 통합이동서비스(MaaS) 해커톤 참가자 모집(~5/3)
                https://okky.kr/article/572953
                '''
            requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')

        # requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={text}')
        # requests.get(api_url + f'/sendMessage?chat_id={chat_id}&text={msg}')

    return '', 200


# app.py 파일이 `python app.py`로시작 되었을 때 작용
if __name__ == '__main__':
    app.run(debug=True)  # 서버가 켜져 있는 동안 수정이 발생하면 자동으로 재시작
