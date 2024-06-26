import sqlite3


def init_db():
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    ''')

    # Create rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def add_booking(room_id, name, date, duration):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO bookings (room_id, name, date, duration)
        VALUES (?, ?, ?, ?)
    ''', (room_id, name, date, duration))

    conn.commit()
    conn.close()


def add_room(room_number, capacity):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO rooms (room_number, capacity)
        VALUES (?, ?)
    ''', (room_number, capacity))

    conn.commit()
    conn.close()


def get_all_rooms():
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()

    conn.close()
    return rooms


def get_bookings_by_name(name):
    conn = sqlite3.connect('booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT b.id, r.room_number, b.name, b.date, b.duration
        FROM bookings b
        INNER JOIN rooms r ON b.room_id = r.id
        WHERE b.name = ?
    ''', (name,))

    bookings = cursor.fetchall()

    conn.close()
    return bookings
