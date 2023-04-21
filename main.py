import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Введите команду в формате:\n' \
           '<имя валюты, цену которой вы хотите узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:\n\n' \
           'Доллар США - USD\n' \
           'Евро - EUR\n' \
           'Российский рубль - RUB'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def handle_message(message: telebot.types.Message):
    try:
        base, quote, amount_text = map(str.upper, message.text.split(' '))
        result = CurrencyConverter.get_price(base, quote, float(amount_text))
        bot.reply_to(message, f'{amount_text} {base} = {result:.2f} {quote}')
    except ValueError:
        bot.reply_to(message, 'Некорректное число')
    except APIException as e:
        bot.reply_to(message, str(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)

