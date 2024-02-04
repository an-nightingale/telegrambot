import telebot
import csv
from telebot import types

token = "mytoken"
bot = telebot.TeleBot(token)

with open('info.txt', 'r', encoding='UTF-8') as f:
    facts = f.read().split('\n')

# Команда start
@bot.message_handler(commands=["start"])
def start(m):
    # Добавление 3 кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Что такое качество жизни?")
    item2 = types.KeyboardButton("Что такое ИЧР?")
    item3 = types.KeyboardButton("Узнать ИЧР в регионе РФ (коэффициент от 0 до 1)")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(m.chat.id, 'Что Вы хотите узнать?', reply_markup=markup)


# Получение сообщений
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global subject, year, waiting_for_subject
    answer = ""
    if message.text.strip() == 'Что такое качество жизни?':
        answer = facts[0]
    elif message.text.strip() == 'Что такое ИЧР?':
        answer = f'{facts[1]}\n{facts[2]}'
    elif message.text.strip() == "Узнать ИЧР в регионе РФ (коэффициент от 0 до 1)":
        waiting_for_subject = True
        bot.send_message(message.chat.id, "Введите название субъекта")
    elif waiting_for_subject:
        subject = message.text.strip()
        waiting_for_subject = False
        bot.send_message(message.chat.id, "Введите год между 2013 и 2019")
    else:
        year = message.text.strip()
        with open('hdi.csv', 'r', encoding="UTF-8") as table:
            reader = csv.DictReader(table, delimiter=';')
            region_found = False
            for row in reader:
                if row['Регион'] == subject:
                    region_found = True
                    if year in row.keys():
                        if row[f"{year}"]:
                            if row[f"{year}"] == "0":
                                answer = "Данные за введенный год не были собраны"
                            else:
                                answer = row[f"{year}"]
                    else:
                        answer = "Год вне диапазона"
            if not region_found:
                answer = "Данные по указанному субъекту не найдены (субъект введен неверно)"
    if answer:
        bot.send_message(message.chat.id, answer)

# Запуск бота
bot.polling(none_stop=True, interval=0)
