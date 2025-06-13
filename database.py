import sqlite3
import os

DB_FILE = "bot_database.db"

def init_db():
    db_exists = os.path.exists(DB_FILE)
    
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            moderator_id INTEGER NOT NULL,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    con.commit()
    con.close()
    
    if not db_exists:
        print("Stworzono nową bazę danych: bot_database.db")
    else:
        print("Baza danych jest już gotowa do akcji, szefie.")

def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                (guild_id, user_id, moderator_id, reason))
    con.commit()
    con.close()

def get_warnings(user_id: int, guild_id: int):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT moderator_id, reason, timestamp FROM warnings WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id))
    warnings = cur.fetchall()
    con.close()
    return warnings