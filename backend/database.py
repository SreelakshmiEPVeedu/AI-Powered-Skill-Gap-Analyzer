# backend/database.py

import sqlite3  #imports python inbuilt sqlite library
import os  #imported to interact with the os
class Database:
    def __init__(self):  #class constructor, automatically runs when Database() created
        self.db_name = "skill_analyzer.db" #stores the database file name
        self._create_tables()  #user-defined funtion toe create tables -  given below
    
    def _create_tables(self):
        try:
            #opens a connection to the sqlite database and assigns connection object to conn
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor() #create a cursor object - excutes sql commands
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')   #command to create a table 
            #list of (username,password) for demo use
            default_users = [
                ("admin", "admin123"),
                ("user", "user123"),
                ("demo", "demo123"),
                ("john", "john123"),
                ("sarah", "sarah123"),
                ("mike", "mike123"),
                ("lisa", "lisa123")
            ]
            #inserting the demo values to the database
            for username, password in default_users:
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                        (username, password)
                    )
                except:
                    pass
            
            conn.commit()  #saves all changes made
            conn.close()   #closes the connection 
            print("✅ Database tables created/verified successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    #function to add a new user 
    def add_user(self, username, password):
        
        try:
            conn = sqlite3.connect(self.db_name) #creates a connection
            cursor = conn.cursor() #creates a cursor
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )   #insert the username and password to the database
            conn.commit()
            conn.close()
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
    #to get the exsisting user
    def get_user(self, username):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()  #selects the first matching row
            conn.close()
            return user  #returns a tuple 
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
   