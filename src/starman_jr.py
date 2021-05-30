import requests
from dotenv import load_dotenv
import os

def send_telegram(message, telegram):
    load_dotenv()
    auth_token = os.getenv('TELEGRAM_TOKEN')
    send_text = f"https://api.telegram.org/bot{auth_token}/sendMessage?chat_id={telegram}&parse_mode=Markdown&text={message}"
    response = requests.get(send_text)
    return 'Message sent via Telegram!'

def send_photo(image_path, image_caption, chat_id):
    load_dotenv()
    auth_token = os.getenv('TELEGRAM_TOKEN')
    data = {"chat_id": chat_id, "caption": image_caption}
    url = f"https://api.telegram.org/bot{auth_token}/sendPhoto"
    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
    return ret.json()