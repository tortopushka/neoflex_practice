from googletrans import Translator
import telebot
from environs import Env

env = Env()
env.read_env()

bot = telebot.TeleBot(env("TOKEN"))

dict_of_lang = {
    'af': 'африкаанс',
    'sq': 'албонского',
    'am': 'амхарского',
    'ar': 'арабского',
    'hy': 'армянского',
    'az': 'азербайджанского',
    'eu': 'баскского',
    'be': 'беларусского',
    'bn': 'бенгальского',
    'bs': 'боснийский',
    "bg": "болгарского",
    "ca": "каталонского",
    "ceb": "кебуано",
    "Нью-Йорк": "чичева",
    'zh-cn': 'китайского (упрощенный)',
    'zh-tw': 'китайского (традиционный)',
    "co": "корсиканец",
    "hr": "хорватского",
    'cs': 'чешского',
    "da": "датского",
    "nl": "голландского",
    "en": "английского",
    "eo": "эсперанто",
    "et": "эстонского",
    "tl": "филиппинского",
    "fi": "финского",
    "fr": "французского",
    "fy": "фризского",
    "gl": "галисийского",
    "ка": "грузинского",
    "de": "немецкого",
    "эль": "греческого",
    "гу": "гуджарати",
    "ht": "гаитянский креольский",
    "ха": "хауса",
    "хоу": "гавайского",
    "iw": "иврита",
    "привет": "хинди",
    "хмн": "хмонг",
    "hu": "венгерского",
    "is": "исландского",
    'ig': 'игбо',
    'id': 'индонезийского',
    "ga": "ирландского",
    "это": "итальянского",
    "ja": "японского",
    "jw": "яванского",
    "кн": "каннада",
    "kk": "казахского",
    "km": "кхмерского",
    "ко": "корейского",
    "ку": "курдского (курманджи)",
    "кы": "кыргызского",
    "ло": "лао",
    "la": "латыни",
    "lv": "латышского",
    "lt": "литовского",
    "lb": "люксембургского",
    "мк": "македонского",
    "mg": "малагасийского",
    "ms": "малайского",
    "ml": "малаялам",
    "mt": "мальтийского",
    "ми": "маори",
    "мистер": "маратхи",
    "mn": "монгольского",
    "мой": "мьянманского (бирманский)",
    "ne": "непальского",
    "нет": "норвежского",
    "ps": "пушту",
    "fa": "персидского",
    "pl": "польского",
    "pt": "португальского",
    "па": "панджаби",
    "ро": "румынского",
    "ru": "русского",
    "sm": "самоанский",
    "gd": "шотландский гэльский",
    "sr": "сербского",
    "st": "сесото",
    'sn': 'шона',
    "sd": "синдхи",
    "си": "сингальского",
    "sk": "словацкого",
    "sl": "словенского",
    "итак": "сомалиец",
    "es": "испанского",
    "су": "сунданского",
    "sw": "суахили",
    "sv": "шведского",
    "tg": "таджикского",
    "та": "тамильского",
    "те": "телугу",
    "th": "тайского",
    "tr": "турецкого",
    "великобритания": "украинского",
    "ur": "урду",
    "uz": "узбекского",
    "vi": "вьетнамского",
    "сай": "валлийского",
    'xh': 'xhosa',
    "йи": "идиш",
    "йо": "йоруба",
    "зу": "зулусского",
    "фил": "филиппинец",
    "он": "иврит"
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Давай начнем! Отправляй мне любое сообщение, а я переведу его на русский язык!')


@bot.message_handler(func=lambda m: True)
def translation_into_Ru(message):
    translator = Translator()
    translated_text = translator.translate(message.text, dest="ru")
    mess = f'{translated_text.text} \n\n(переведено с {dict_of_lang[translated_text.src]})'
    bot.reply_to(message, mess)


bot.infinity_polling()