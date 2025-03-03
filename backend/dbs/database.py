import sqlite3 as sql

class Database:
    def __init__(self):
        self.db_path = "./backend/dbs/SCdb.db"
        self.create_tables()

    def create_tables(self):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    uniqueid INTEGER,
                    userid INTEGER,
                    username TEXT)""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages(
                    messageid INTEGER PRIMARY KEY AUTOINCREMENT,
                    fromuserid INTEGER,
                    userid INTEGER,
                    message TEXT,
                    view INTEGER DEFAULT 0)""")
            conn.commit()

    def add_user(self, uniqueid, userid, username):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,)).fetchall():
                return
            cursor.execute("INSERT INTO users(uniqueid, userid, username) VALUES(?, ?, ?)", (uniqueid, userid, username))
            conn.commit()

    def getstats(self, userid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            received_count = cursor.execute("SELECT COUNT(*) FROM messages WHERE userid = ? AND view = 1", (userid,)).fetchone()[0]
            sent_count = cursor.execute("SELECT COUNT(*) FROM messages WHERE fromuserid = ?", (userid,)).fetchone()[0]
            return received_count, sent_count

    def add_message(self, fromuserid, userid, message):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (fromuserid, userid, message) VALUES (?, ?, ?)", (fromuserid, userid, message))
            conn.commit()

    def get_messages(self, userid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT * FROM messages WHERE userid = ? AND view = 0", (userid,)).fetchall()

    def update_message_view(self, messageid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE messages SET view = 1 WHERE messageid = ?", (messageid,))
            conn.commit()

    def get_last_msgid(self, userid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT messageid FROM messages WHERE userid = ? ORDER BY messageid DESC LIMIT 1", (userid,)).fetchone()[0]

    def get_user(self, userid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,)).fetchall() or None
    
    def get_user_uniqueid(self, uniqueid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT userid FROM users WHERE uniqueid = ?", (uniqueid,)).fetchone()[0] or None

    def get_uniqueid(self, userid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT uniqueid FROM users WHERE userid = ?", (userid,)).fetchone()[0]

    def check_uniqueid(self, uniqueid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT * FROM users WHERE uniqueid = ?", (uniqueid,)).fetchone() is not None

    def update_uniqueid(self, userid, new_uniqueid):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET uniqueid = ? WHERE userid = ?", (new_uniqueid, userid))
            conn.commit()

db = Database()