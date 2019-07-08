from telegram.ext import *

from datetime import time

import os, logging

import dialog
import secret

from database import *
from user     import *

from service import Service, ServiceAdd
from game    import Game

logging.basicConfig(format="%(message)s", level=logging.INFO)

request_kwargs = {
    "proxy_url": "socks5://t.geekclass.ru:7777",
    "urllib3_proxy_kwargs": { "username": "geek", "password": "socks" }
}

class Bot:
    def __init__(self, token, dbfile = "bot.sqlite", request_kwargs = request_kwargs):
        self.dbfile = dbfile
        self.active = {}

        updater = Updater(token=token, request_kwargs=request_kwargs)

        dispatcher = updater.dispatcher
        job_queue  = updater.job_queue

        handler_start   = CommandHandler("start",       self.start)
        handler_help    = CommandHandler("help",        self.help)
        handler_names1  = CommandHandler("names1",      self.names1)
        handler_names2  = CommandHandler("names2",      self.names2)
        handler_account = CommandHandler("account",     self.account)
        handler_new     = CommandHandler("new",         self.new)
        handler_add     = CommandHandler("add",         self.add)
        handler_text    = MessageHandler(Filters.text,  self.text)
        handler_photo   = MessageHandler(Filters.photo, self.photo)

        dispatcher.add_handler(handler_start)
        dispatcher.add_handler(handler_help)
        dispatcher.add_handler(handler_names1)
        dispatcher.add_handler(handler_names2)
        dispatcher.add_handler(handler_account)
        dispatcher.add_handler(handler_new)
        dispatcher.add_handler(handler_add)
        dispatcher.add_handler(handler_text)
        dispatcher.add_handler(handler_photo)

        updater.start_polling()

    def start(self, bot, update):
        DataBase(self.dbfile).add_user(User(update.message.chat_id))
        bot.send_message(chat_id=update.message.chat_id, text=dialog.start)

    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=dialog.help)

    def names1(self, bot, update):
        user, game = self.get_user(update.message.chat_id)

        try:
            game = Game(self.dbfile, user, level = 1)
            self.active[user] = game
            game.play(bot, update)
        except IndexError:
            bot.send_message(user.chat_id, dialog.game_nobody)
            del self.active[user]

    def names2(self, bot, update):
        user, game = self.get_user(update.message.chat_id)

        game = Game(self.dbfile, user, level = 2)
        self.active[user] = game
        game.play(bot, update)

    def account(self, bot, update):
        try:
            account = DataBase(self.dbfile).get_account(update.message.chat_id)
            bot.send_message(update.message.chat_id, dialog.account_success % dialog.gotubles(account))
        except DataNotFoundError:
            bot.send_message(update.message.chat_id, dialog.account_fail)

    def new(self, bot, update):
        if DataBase(self.dbfile).get_admin(update.message.chat_id):
            if os.path.exists(self.dbfile):
                if os.path.exists(self.dbfile + ".old"):
                    os.remove(self.dbfile + ".old")
                os.rename(self.dbfile, self.dbfile + ".old")

            DataBase(self.dbfile)

            bot.send_message(update.message.chat_id, dialog.new_success)

    def add(self, bot, update):
        user, activity = self.get_user(update.message.chat_id)

        if user.admin:
            service = ServiceAdd(self.dbfile, user)
            self.active[user] = service
            service.run(bot, update)

    def text(self, bot, update):
        user, activity = self.get_user(update.message.chat_id)

        if isinstance(activity, Game):
            activity.play(bot, update)
        elif isinstance(activity, Service):
            activity.run(bot, update)
        elif update.message.text == secret.password:
            user.admin = True
            DataBase(self.dbfile).set_admin(user)
            bot.send_message(user.chat_id, dialog.admin)
        else:
            bot.send_message(user.chat_id, dialog.dunno)

        if activity and activity.step == None:
            del self.active[user]

    def photo(self, bot, update):
        user, activity = self.get_user(update.message.chat_id)

        if isinstance(activity, Service):
            activity.run(bot, update)
        else:
            bot.send_message(user.chat_id, dialog.dunno)

        if activity and activity.step == None:
            del self.active[user]

    def get_user(self, chat_id):
        for user in self.active.keys():
            if user.chat_id == chat_id:
                return user, self.active[user]
        try:
            return DataBase(self.dbfile).get_user(chat_id), None
        except DataNotFoundError:
            user = User(chat_id)
            DataBase(self.dbfile).add_user(user)
            return user, None

if __name__ == "__main__":
    Bot(secret.token)
