import telebot 
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username  # Переменная объявлена в начале функции

    if username not in Pokemon.pokemons.keys():
        # Создание нового покемона
        pokemon = Pokemon(username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        # Если покемон уже существует
        existing_pokemon = Pokemon.pokemons[username]
        bot.reply_to(
            message, 
            f"Ты уже создал себе покемона. Вот он:\n{existing_pokemon.info()}"
        )
        bot.send_photo(message.chat.id, existing_pokemon.show_img())

@bot.message_handler(commands=['level_up'])
def level_up(message):
    username = message.from_user.username

    if username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[username]
        pokemon.level_up()
        bot.send_message(
            message.chat.id,
            f"{pokemon.name} повысил уровень до {pokemon.level}!\n"
            f"Новая информация:\n{pokemon.info()}"
        )
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")



bot.infinity_polling(none_stop=True)

