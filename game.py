import os, json, random, time

from database import *
from keyboard import *

import dialog

class Game:
    def __init__(self, dbfile, user, level):
        self.dbfile = dbfile
        self.user   = user
        self.level  = level
        self.score  = 0
        self.step   = 0
        self.right  = None

        gotoers = DataBase(self.dbfile).get_gotoers()

        self.photos = [x[0] for x in gotoers]
        self.names  = [x[1] for x in gotoers]

        with open("names.json") as f:
            self.namedict = { uniform(x) : tuple(map(uniform, y)) for x, y in json.load(f).items() }

    def play(self, bot, update):
        if self.step == 0:
            if self.level == 1:
                rules = dialog.game_rules_1
            if self.level == 2:
                rules = dialog.game_rules_2

            bot.send_message(self.user.chat_id, rules)

            self.step = 1
            self.play(bot, update)

        elif self.step == 4:
            self.check(bot, update)

            text = dialog.game_result % dialog.gotubles(self.score)
            bot.send_message(self.user.chat_id, text, reply_markup = no_keyboard)

            self.user.account += self.score
            self.step          = None

            DataBase(self.dbfile).update_account(self.user)

        else:
            if self.step != 1:
                self.check(bot, update)

            time.sleep(1)

            photo = random.choice(self.photos)
            while True:
                variants = random.choices(self.names, k = 2)
                right    = DataBase(self.dbfile).get_first_name(photo)
                variants.append(right)

                if not has_duplicates(variants):
                    break

            random.shuffle(variants)

            if self.level == 1:
                markup = keyboard([variants])
            if self.level == 2:
                markup = no_keyboard

            bot.send_photo(self.user.chat_id, photo, reply_markup = markup)

            self.step += 1

            try:
                self.right = (uniform(right), ) + self.namedict[uniform(right)]
            except KeyError:
                self.right = (uniform(right), )

    def check(self, bot, update):
        if uniform(update.message.text) in self.right:
            self.score += self.level
            bot.send_message(self.user.chat_id, dialog.game_success)
        else:
            bot.send_message(self.user.chat_id, dialog.game_fail % self.right[0])

def has_duplicates(container):
    res  = False
    seen = []

    for elem in container:
        if elem in seen:
            res = True
            break
        else:
            seen.append(elem)

    return res

uniform = lambda name: name.capitalize().replace("ё", "е")
