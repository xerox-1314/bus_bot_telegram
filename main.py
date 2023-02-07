import config
import telebot
from telebot import types
from functions import create_all_stops, next_bus_on_city, next_bus_on_pol, timetable_today, timetable

# создание объекта бота с указанием токена
token = config.TOKEN
bot = telebot.TeleBot(token)

# реализация команд бота
@bot.message_handler(commands=['start'])
def welcome_message(message):
    hello_sticker = open('D:/Program Files/pycharmprograms/hello_sticker.webp', 'rb') # здесь любой стикер Привееет!!
    bot.send_sticker(message.chat.id, hello_sticker)
    bot.send_message(message.chat.id, 'Привет! Если ты здесь, значит ты живешь на лесной поляне. Я бот, который поможет тебе добраться до лесной поляны или в город из нее! Вот список моих команд:\n' +
                                      '/help - вызвать список команд\n/go - узнать ближайшее прибытие автобуса на твою остановку\n/timetoday - узнать расписание сегодня в течение дня на выбранной остановке\n' +
                                      '/info - узнать информацию об автобусах 170э, 171э, 172э и 173э\n/timetable - узнать распиание в какой-то другой день на выбранной остановке',
                                      parse_mode='html')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Вот список моих команд:\n' + '/help - вызвать список команд\n/go - узнать ближайшее прибытие автобуса на твою остановку\n/timetoday - узнать расписание автобусов сегодня в течение дня на выбранной остановке\n'+
                                      '/info - узнать информацию об автобусах 170э, 171э, 172э и 173э\n/timetable - узнать распиание в какой-то другой день на выбранной остановке',
                                      parse_mode='html')

@bot.message_handler(commands=['go'])
def go_message1(message):
    stops = create_all_stops()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in stops:
        item = types.KeyboardButton(i)
        markup.add(item)
    k = bot.send_message(message.chat.id, 'Выбери остановку', reply_markup=markup)
    bot.register_next_step_handler(k, go_message2)
def go_message2(message):
    global stop
    stop = message.text
    delete_keyboard = telebot.types.ReplyKeyboardRemove()
    z = bot.send_message(message.chat.id, 'А теперь скажи, куда хочешь попасть (в город/на поляну)', reply_markup=delete_keyboard)
    bot.register_next_step_handler(z, go_message3)
def go_message3(message):
    line = message.text
    if line == 'в город':
        bot.send_message(message.chat.id, next_bus_on_city(stop))
    elif line == 'на поляну':
        bot.send_message(message.chat.id, next_bus_on_pol(stop))
    else:
        open_sticker = open('D:/Program Files/pycharmprograms/chel_ty_v_myte.webp', 'rb')
        bot.send_sticker(message.chat.id, open_sticker)
        bot.send_message(message.chat.id, 'Что-то пошло не так..... Я же попросил тебя, либо в город, либо на поляну')

@bot.message_handler(commands=['timetoday'])
def time_message1(message):
    stops = create_all_stops()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in stops:
        item = types.KeyboardButton(i)
        markup.add(item)
    mes1 = bot.send_message(message.chat.id, 'Выбери остановку, на которую хочешь узнать распиание на сегодняшний день', reply_markup=markup)
    bot.register_next_step_handler(mes1, time_message2)
def time_message2(message):
    global chose_stop
    chose_stop = message.text
    delete_keyboard = telebot.types.ReplyKeyboardRemove()
    mes2 = bot.send_message(message.chat.id, 'А теперь скажи, в какую сторону тебе надо рассматривать расписание (в город/на поляну)', reply_markup=delete_keyboard)
    bot.register_next_step_handler(mes2, time_message3)
def time_message3(message):
    line = message.text
    if line != 'в город' and line != 'на поляну':
        open_sticker = open('D:/Program Files/pycharmprograms/chel_ty_v_myte.webp', 'rb')
        bot.send_sticker(message.chat.id, open_sticker)
        bot.send_message(message.chat.id, 'Что-то пошло не так..... Я же попросил тебя, либо в город, либо на поляну')
    else:
        bot.send_message(message.chat.id, timetable_today(chose_stop, line))

@bot.message_handler(commands=['timetable'])
def timetable1(message):
    stops = create_all_stops()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in stops:
        item = types.KeyboardButton(i)
        markup.add(item)
    mes1 = bot.send_message(message.chat.id, 'Хорошо, выбери остановку', reply_markup=markup)
    bot.register_next_step_handler(mes1, timetable2)
def timetable2(message):
    global stop
    stop = message.text
    delete_keyboard = telebot.types.ReplyKeyboardRemove()
    mes2 = bot.send_message(message.chat.id, 'А теперь скажи день, на который хочешь узнать расписание (в формате ГГГГ-ММ-ДД (пр.: 2022-01-29))', reply_markup=delete_keyboard)
    bot.register_next_step_handler(mes2, timetable3)
def timetable3(message):
    global data
    data = message.text
    mes3 = bot.send_message(message.chat.id, 'И еще, в какую сторону тебе нужно (в город/на поляну)')
    bot.register_next_step_handler(mes3, timetable4)
def timetable4(message):
    line = message.text
    if line != 'в город' and line != 'на поляну':
        open_sticker = open('D:/Program Files/pycharmprograms/chel_ty_v_myte.webp', 'rb')
        bot.send_sticker(message.chat.id, open_sticker)
        bot.send_message(message.chat.id, 'Что-то пошло не так..... Я же попросил тебя, либо в город, либо на поляну')
    else:
        bot.send_message(message.chat.id, timetable(stop, data, line))
@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, 'Автобус 170э: Поляна - Вокзал\nАвтобус 171э: Поляна - Шалготарьян\nАвтобус 172э: Поляна - Лапландия\nАвтобус 173э: Поляна - Радуга',
                     parse_mode='html')

@bot.message_handler(content_types=['text'])
def error_message(message):
    stick = open('D:/Program Files/pycharmprograms/senya.webp', 'rb')
    bot.send_sticker(message.chat.id, stick)
    bot.send_message(message.chat.id, 'Я подумаю над этим... Но реагировать на команды у меня получается лучше')


bot.polling(none_stop=True, interval=0)