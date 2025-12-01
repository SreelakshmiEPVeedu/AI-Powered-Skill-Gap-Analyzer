# backend/database.py

import sqlite3

class Database:
    def __init__(self):
        self.db_name = "skill_analyzer.db"
        self._create_tables()
    
    def _create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            default_users = [
                ("admin", "admin123"),
                ("user", "user123"),
                ("demo", "demo123"),
                ("john", "john123"),
                ("sarah", "sarah123"),
                ("mike", "mike123"),
                ("lisa", "lisa123")
            ]
            
            for username, password in default_users:
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                        (username, password)
                    )
                except:
                    pass
            
            conn.commit()
            conn.close()
            print("✅ Database tables created/verified successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    
    def add_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            return False
    
    def get_user(self, username):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
