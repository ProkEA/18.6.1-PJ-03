import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter, DeclensionByCases

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите команду в формате:\n <имя валюты цену которой Вы хотите узнать> ' \
           '<в какую валюту Вы хотите перевести> <количество переводимой валюты> \n' \
           'Увидеть доступные валюты /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        words = message.text.split(' ')

        if len(words) != 3:
            raise ConvertionException('Неверные параметры.')

        quote, base, amount = words
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        inclined_quote = DeclensionByCases(quote, float(amount))
        inclined_base = DeclensionByCases(base, float(total_base))
        quote = inclined_quote.incline()
        base = inclined_base.incline()
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
