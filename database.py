import sqlite3

from user import *

class DataBase:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn   = sqlite3.connect(dbfile)

        stmt = "CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY, account INTEGER, admin INTEGER)"

        self.conn.execute(stmt)

        stmt = "CREATE TABLE IF NOT EXISTS gotoers (photo TEXT PRIMARY KEY, first_name TEXT, last_name TEXT)"

        self.conn.execute(stmt)
        self.conn.commit()

    def add_user(self, user):
        stmt = "INSERT OR IGNORE INTO users (chat_id, account, admin) VALUES (?, ?, ?)"
        args = (user.chat_id, user.account, user.admin)

        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_user(self, chat_id):
        stmt = "SELECT * FROM users WHERE chat_id = (?)"
        args = (chat_id, )

        try:
            chat_id, account, admin = [x for x in self.conn.execute(stmt, args)][0]
            return User(chat_id, account = account, admin = admin)
        except IndexError:
            raise DataNotFoundError("Cannot find user with chat_id = %d" % chat_id)

    def update_account(self, user):
        stmt = "UPDATE users SET account = (?) WHERE chat_id = (?)"
        args = (user.account, user.chat_id)

        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_account(self, chat_id):
        stmt = "SELECT account FROM users WHERE chat_id = (?)"
        args = (chat_id, )

        try:
            return [x[0] for x in self.conn.execute(stmt, args)][0]
        except IndexError:
            raise DataNotFoundError("Cannot find user with chat_id = %d" % chat_id)

    def set_admin(self, user):
        stmt = "UPDATE users SET admin = (?) WHERE chat_id = (?)"
        args = (user.admin, user.chat_id)

        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_admin(self, chat_id):
        stmt = "SELECT admin FROM users WHERE chat_id = (?)"
        args = (chat_id, )

        try:
            return [x[0] == 1 for x in self.conn.execute(stmt, args)][0]
        except IndexError:
            raise DataNotFoundError("Cannot find user with chat_id = %d" % chat_id)

    def add_gotoer(self, photo, first_name, last_name):
        stmt = "INSERT INTO gotoers (photo, first_name, last_name) VALUES (?, ?, ?)"
        args = (photo, first_name, last_name)

        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_gotoers(self):
        stmt = "SELECT * FROM gotoers"

        return [x for x in self.conn.execute(stmt)]

    def get_first_name(self, photo):
        stmt = "SELECT first_name FROM gotoers WHERE photo = (?)"
        args = (photo, )

        try:
            return [x[0] for x in self.conn.execute(stmt, args)][0]
        except IndexError:
            raise DataNotFoundError("Cannot find gotoer with photo = %s" % photo)

class DataBaseError(Exception):
    pass

class DataNotFoundError(DataBaseError):
    pass
