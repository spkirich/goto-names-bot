from telegram import *

keyboard = lambda buttons: ReplyKeyboardMarkup(
        [[KeyboardButton(x) for x in xs] for xs in buttons],
        one_time_keyboard = True
    )

no_keyboard = ReplyKeyboardRemove()
