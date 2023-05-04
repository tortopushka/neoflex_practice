from googletrans import Translator
import telebot
import utils
from models.models import *
from db_session import env, session
import datetime
import alembic.config
import os
import speech_recognition as sr
import soundfile as sf


recognizer = sr.Recognizer()
bot = telebot.TeleBot(env("TOKEN"))


def create_cache(text_of_message: Text, language_code: String, translated_text: Text):
    cache = Cache()
    cache.text_of_message = text_of_message
    cache.language_code = language_code
    cache.date_of_activity = datetime.datetime.now()
    cache.russian_translation = translated_text
    session.add(cache)
    session.commit()


def translation_into_ru(text_mess):
    check_cache = session.query(Cache.russian_translation, Cache.language_code) \
        .filter(Cache.text_of_message == text_mess).first()
    if check_cache is None:
        translator = Translator()
        translated_text = translator.translate(text_mess, dest="ru")
        mess = f'{translated_text.text} \n\n(переведено с {utils.dict_of_lang[translated_text.src]})'
        create_cache(text_mess, translated_text.src, translated_text.text)
    else:
        mess = f'{check_cache.russian_translation} \n\n(переведено с {utils.dict_of_lang[check_cache.language_code]})'
    session.close()
    return mess


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_text, language='en-GB')
            return text
        except:
            return "Sorry.. run again..."


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Давай начнем! Отправляй мне любое сообщение, а я переведу его на русский язык!')


@bot.message_handler(func=lambda m: True)
def text_processing(message):
    bot.reply_to(message, translation_into_ru(message.text))


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    filename = str(file_info.file_id)
    file_name_full = "./voice/"+filename+".ogg"
    file_name_full_converted = "./ready/"+filename+".wav"

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)

    data, samplerate = sf.read(file_name_full)
    sf.write(file_name_full_converted, data, samplerate)

    text = recognise(file_name_full_converted)
    if text == "Sorry.. run again...":
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, translation_into_ru(text))
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


if __name__ == "__main__":
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    #alembic.config.main(argv=alembicArgs)
    bot.infinity_polling()
