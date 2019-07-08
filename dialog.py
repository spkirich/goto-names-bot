start = """
Привет!
Я GoToEventBot, и я помогу тебе знакомиться и запомнинать имена людей в лагере )
Нажми сюда, чтобы узнать о возможностях: /help.
"""

help = """
/start   - перезапустить бота
/names1  - игра на запоминание имён
/names2  - более сложная игра на запоминание имён
/account - узнать свой баланс
"""

dunno   = "Эмм... не совсем понял... /help, кстати, всегда помогает..."

playing = "Ты уже в игре, так что сначала закончи её!"

game_rules_1 = "Я буду показывать тебе фото человека, а ты - указывать его имя.\nПоехали!"
game_rules_2 = "Я буду показывать тебе фото человека, а ты - писать его имя.\nПоехали!"
game_success = "Правильно!"
game_fail    = "Неправильно, это %s..."
game_result  = "Твой результат: %d %s.\nСыграть ещё: /names1."
game_nobody  = "Эмм... Тут проблема: орги пока не заполнили базу данных..."

account_success = "У тебя на счету %d %s."
account_fail    = "Похоже, ты не заводил здесь свой счёт...\nСыграй в игру: /names1."

admin = "Администраторские права предоставлены!"

new_success = "Новая база данных введена успешно!"

add_last_name  = "Как его/её фамилия?"
add_first_name = "Как его/её имя?"
add_photo      = "Жду фото..."
add_success    = "Zapomnil..."

def gotubles(n):
    if n % 10 == 1 and n != 11:
        return (n, "готубль")
    elif (n % 10 > 1 and n % 10 < 5) and (n < 10 or n > 20):
        return (n, "готубля")
    else:
        return (n, "готублей")
