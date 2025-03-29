import sqlite3

class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

class Event:
    def __init__(self, id, name, date, place, owner_id):
        self.id = id
        self.name = name
        self.date = date
        self.place = place
        self.owner_id = owner_id

def create_database():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (            
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            place TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_event (
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,            
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            PRIMARY KEY (user_id, event_id)
        )
    ''')

    conn.commit()
    conn.close()

def create_event(name, date, place, owner_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name, date, place, owner_id) VALUES (?, ?, ?, ?)", (name, date, place, owner_id))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return Event(event_id, name, date, place, owner_id)

def get_all_events():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    events = [Event(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    return events

def create_user(username):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return User(user_id, username)

def get_all_users():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()    
    users = [User(row[0], row[1]) for row in rows]    
    return users    

def register_user_for_event(user_id, event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_event (user_id, event_id) VALUES (?, ?)", (user_id, event_id))
    conn.commit()
    conn.close()

def get_user_events(user_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.* FROM events e
        JOIN user_event ue ON e.id = ue.event_id
        WHERE ue.user_id = ?
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    events = [Event(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    return events

create_database()