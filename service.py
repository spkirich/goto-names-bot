import os, dialog

from database import DataBase

class Service:
    def __init__(self, dbfile, user):
        self.dbfile = dbfile
        self.user   = user
        self.step   = 0

    def run(self, bot, update):
        raise NotImplementedError

class ServiceAdd(Service):
    def __init__(self, dbfile, user):
        super().__init__(dbfile, user)

        self.first_name = None
        self.last_name  = None
        self.photo      = None

    def run(self, bot, update):
        if self.step == 0:
            bot.send_message(self.user.chat_id, dialog.add_last_name)
        elif self.step == 1:
            self.last_name = update.message.text
            bot.send_message(self.user.chat_id, dialog.add_first_name)
        elif self.step == 2:
            self.first_name = update.message.text
            bot.send_message(self.user.chat_id, dialog.add_photo)
        elif self.step == 3:
            self.photo = update.message.photo[-1].file_id

            DataBase(self.dbfile).add_gotoer(self.photo, self.first_name, self.last_name)

            bot.send_message(self.user.chat_id, dialog.add_success)

            self.step = None
            return

        self.step += 1
