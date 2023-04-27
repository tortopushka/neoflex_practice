from googletrans import Translator
import telebot
from environs import Env
import utils
from models.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

env = Env()
env.read_env()

bot = telebot.TeleBot(env("TOKEN"))


def create_cache(session, text_of_message, language_code, date_of_activity, translated_text):
    cache = Cache()
    cache.text_of_message = text_of_message
    cache.language_code = language_code
    cache.date_of_activity = datetime.datetime.utcfromtimestamp(date_of_activity)
    cache.russian_translation = translated_text
    session.add(cache)
    session.commit()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Давай начнем! Отправляй мне любое сообщение, а я переведу его на русский язык!')


@bot.message_handler(func=lambda m: True)
def translation_into_ru(message):
    session_maker = sessionmaker(bind=create_engine(env("URL")))
    session = session_maker()
    check_cache = session.query(Cache.russian_translation, Cache.language_code)\
        .filter(Cache.text_of_message==message.text).first()
    if check_cache is None:
        translator = Translator()
        translated_text = translator.translate(message.text, dest="ru")
        mess = f'{translated_text.text} \n\n(переведено с {utils.dict_of_lang[translated_text.src]})'
        create_cache(session, message.text, translated_text.src, message.date, translated_text.text)
    else:
        mess = f'{check_cache.russian_translation} \n\n(переведено с {utils.dict_of_lang[check_cache.language_code]})'
        print(check_cache.russian_translation)
    session.close()
    bot.reply_to(message, mess)


if __name__ == "__main__":
    bot.infinity_polling()
