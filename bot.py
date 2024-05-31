import telebot
import parse

channels = parse.get_main_channels()

bot = telebot.TeleBot("7495969276:AAFHtBJnh6hgyNa5K_-EeCjHuSlQotYXAMs")

@bot.message_handler(commands = ["start"])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    help_btn = telebot.types.InlineKeyboardButton("Справка по командам", callback_data="help")
    markup.add(help_btn)
    bot.send_message(message.chat.id, """Привет!!! Этот бот помогает получать различную информацию о фильмах и телепередаче.
Чтобы получить подробуную справку по всем доступным командам - введите команду /help.""", reply_markup=markup)
    

@bot.message_handler(commands = ["help", "info"])
def help(message):
    comands = {"/start": "Поздороваться",
               "/help": "Получить информацию по всем командам",
               "/channel": "Получить телепрограмму определенного канала",
               "/live": "Получить телепрограмму всех каналов на текущий момент времени",
               "/film": "Получить информацию о введенном фильме",
               "/tvcategory": "Получить все программы определённой категории идущие в текущий момент времени",
               "/genre": "Получить все программы определённого жанра идущие в текущий момент времени",}
    s = "Список всех доступных команд:\n"
    for comand, description in comands.items():
        s += comand + ": " + description + '\n'
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands = ["live"])
def live(message):
    global channels
    p = parse.get_actual_programs(channels)
    s = "Телепрограмма:\n"
    for i in p:
        s += i + "\n"
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands = ["channel"])
def channel(message):
    bot.send_message(message.chat.id, "Введите название канала")
    bot.register_next_step_handler(message, channel_program)

def channel_program(message):
    title = (message.text.strip()).upper()
    if title not in channels.keys():
        bot.send_message(message.chat.id, "Название канала введено с ошибкой или такого канала не существует")
        return
    s = ""
    for i in parse.get_list_programs(channels[title]):
        s += i + '\n'
    bot.send_message(message.chat.id, s)


@bot.message_handler(commands = ["tvcategory"])
def category(message):
    bot.send_message(message.chat.id, "Введите желаемую категорию программы")
    bot.register_next_step_handler(message, get_categories)

def get_categories(message):
    category = (message.text.strip()).upper()
    bot.send_message(message.chat.id, "Ищу программы...")
    p = parse.get_actual_programs_info(channels)
    programs = []
    for k, v in p.items():
        if v.category.upper() == category:
            programs.append(k + ": " + v.title)
    
    if len(programs) == 0:
        bot.send_message(message.chat.id, "Название категории введено с ошибкой или таких программ сейчас не идёт")
        return
    s = ""
    for i in programs:
        s += i + '\n'
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands = ["genre"])
def genre(message):
    bot.send_message(message.chat.id, "Введите желаемый жанр программы")
    bot.register_next_step_handler(message, get_genre)

def get_genre(message):
    genre = (message.text.strip()).upper()
    bot.send_message(message.chat.id, "Ищу программы...")
    p = parse.get_actual_programs_info(channels)
    programs = []
    for k, v in p.items():
        if genre in [x.upper() for x in v.genre]:
            programs.append(k + ": " + v.title)
    
    if len(programs) == 0:
        bot.send_message(message.chat.id, "Название жанра введено с ошибкой или таких программ сейчас не идёт")
        return
    s = ""
    for i in programs:
        s += i + '\n'
    bot.send_message(message.chat.id, s)


@bot.message_handler(commands = ["film"])
def film(message):
    bot.send_message(message.chat.id, "Введите название фильма или его краткое описание")
    bot.register_next_step_handler(message, get_film_info)

def get_film_info(message):
    s = ""
    kp, imdb = parse.get_rating(message.text)
    if kp is None:
        s += "Рейтинг на Кинопоиске неопределён\n"
    else:
        s += f"Рейтинг на Кинопоиске: {kp}\n"
    if imdb is None:
        s += "Рейтинг на IMDB неопределён\n"
    else:
        s += f"Рейтинг на IMDB: {imdb}\n"
    url = parse.get_url_from_kp(message.text)
    if url == 0:
        bot.send_message(message.chat.id, "Не удалось найти такой фильм")
    else:
        bot.send_message(message.chat.id, f"https://www.kinopoisk.ru{url}")
        bot.send_message(message.chat.id, s)

@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == 'help':
        help(callback.message)

bot.infinity_polling()