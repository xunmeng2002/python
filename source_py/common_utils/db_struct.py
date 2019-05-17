# encoding: utf-8


class DbInfo:
    def __init__(self, admin_db, history_db, init_db, sync_db):
        self.admin_db = admin_db
        self.history_db = history_db
        self.init_db = init_db
        self.sync_db = sync_db
        self.admin_tables = {}
        self.history_tables = {}
        self.init_tables = {}
        self.sync_tables = {}
