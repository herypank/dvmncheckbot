import os
from time import sleep
from dotenv import load_dotenv
import requests
import telegram


def send_request(url, payload):
        AUTH_HEADERS = {'Authorization':DVMN_TOKEN}
        response = requests.get(url, headers=AUTH_HEADERS, params=payload)
        return response.json()


if __name__ == "__main__":
    url = 'https://dvmn.org/api/long_polling/'
    load_dotenv()
    DVMN_TOKEN = os.getenv('DVMN_TOKEN')
    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    payload = {"timestamp":''}
    chat_id = os.getenv("CHAT_ID")
    while True:
        try:
            api_mess = send_request(url, payload)
        except requests.exceptions.ReadTimeout:
            print ('Ошибка на сервере DevMan.')
        except ConnectionError:
            print('Проверьте соединение с интернетом.')
        if api_mess['status'] == 'timeout':
            payload['timestamp'] = api_mess['timestamp_to_request']
        elif api_mess['status'] == 'found':
            payload['timestamp'] = api_mess['last_attempt_timestamp']
            important_messages = api_mess["new_attempts"][0]
            text_mess = f'''У вас проверили работу <<{important_messages['lesson_title']}>>
            
            '''
            bot.send_message(chat_id=chat_id, text=text_mess)
        sleep(1)