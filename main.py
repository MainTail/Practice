import telebot
token = '6313227161:AAFCPAQwNJJrl7xekZA0ORhyjezt_YsgWyU'
bot = telebot.TeleBot(token)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Приветствую {message.from_user.first_name}!")
    bot.send_message(message.chat.id, "Если готов решить викторину, то отправь команду /quiz")


user_states = {}  # Инициация пустого словаря


# Обработчик команды /quiz
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    chat_id = message.chat.id  # Уникальное значение чата
    user_states[chat_id] = 1  # Занесение значения в словарь и присвивание значение 1
    send_question(chat_id, user_states[chat_id])  # Отрправление 1го вопроса


# Функция для отправки вопроса
def send_question(chat_id, question_number):
    question = get_question_by_number(question_number)  # Получение вопроса по его номеру
    bot.send_message(chat_id, question)


# Функция, которая возвращает вопрос по его номеру
def get_question_by_number(question_number):
    if question_number == 1:
        return "Чему равно 2*2?"
    elif question_number == 2:
        return "Как называется столица Франции?"


# Обработка ответов на вопросы
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    chat_id = message.chat.id
    if chat_id in user_states and user_states[chat_id] is not None:  # Проверка на участие пользователя в викторине
        if user_states[chat_id] == 1 and message.text == "4":
            bot.reply_to(message, "Верно!")
        elif user_states[chat_id] == 1 and message.text != "4":
            bot.reply_to(message, "Не верно!")
        if user_states[chat_id] == 2 and message.text.lower() == "париж":
            bot.reply_to(message, "Верно!")
        elif user_states[chat_id] == 2 and message.text.lower() != "париж":
            bot.reply_to(message, "Не верно!")
        user_states[chat_id] += 1  # Переход к следующему вопросу или завершаем викторину
        if user_states[chat_id] <= 2:
            send_question(chat_id, user_states[chat_id])  # Отправка следующий вопрос


def run_bot():               # Функция для запуска бота
    bot.infinity_polling()


if __name__ == "__main__":
    run_bot()
