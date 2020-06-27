import telebot
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot('991250362:AAH4Vr-plqYCkqhO8350NkaZbmcysj1-2zA')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id, f'Hello, {message.from_user.username}! Nice to meet you here.')
    bot.send_message(message.from_user.id, 'Type me the link of the VK profile which you want to parse')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'Loading...')
    try:
        soup = BeautifulSoup(requests.get(message.text).content, 'html.parser')

        hr = soup.select('#wide_column > div:nth-child(1) > div.counts_module > a:nth-child(3)')[0].get('href')

        p_url = 'https://vk.com' + hr
        soup_2 = BeautifulSoup(requests.get(p_url).text, 'html.parser')

        photos_2 = soup_2.find_all('div', {'class': 'photos_row'})

        all_photos = [i.get('style') for i in photos_2]

        for i in all_photos:
            bot.send_photo(message.from_user.id, requests.get(i[22:i.index(';') - 1]).content)

    except Exception:
        bot.send_message(message.from_user.id, "I can't send you photos :(")


bot.polling()
