class User:
    def __init__(self, chat_id, account = 0, admin = False):
        self.chat_id = chat_id
        self.account = account
        self.admin   = admin
