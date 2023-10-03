import telebot

from settings import TOKEN, keys
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def command_help(message: telebot.types.Message):
    text = ('Чтобы начать, Вы должны отправить сообщение боту в виде <Имя валюты, цену которой вы хотите узнать> <Имя \
валюты, в которой надо узнать цену первой валюты> <Количество первой валюты> \n'
            'Для начала вы можете используйте комманду /values!')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        split = message.text.split()

        if len(split) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = split
        total_base = CurrencyConverter.convert(quote, base, amount)
        converted_amount = float(amount) * total_base
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e} ')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {converted_amount}'
        bot.send_message(message.chat.id, text)


bot.polling()
