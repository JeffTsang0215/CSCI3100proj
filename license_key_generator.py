from shared import path
import sqlite3
import random
import string


def generate_key():
    """Generate a single license key in the format AAAA-BBBB-CCCC-DDDD"""
    chars = string.ascii_uppercase + string.digits
    segments = []
    for _ in range(3):
        segment = ''.join(random.choices(chars, k=4))
        segments.append(segment)
    return '-'.join(segments)


def create_database():
    """Create database and table if they don't exist"""
    conn = sqlite3.connect(path + 'database/database.db')
    cursor = conn.cursor()
    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS licenses
                        (license_key TEXT PRIMARY KEY UNIQUE,
                         is_consumed BOOLEAN DEFAULT 0)''')

    conn.commit()
    conn.close()


def generate_keys(num_keys):
    """Generate and store unique license keys in the database"""
    conn = sqlite3.connect(path + 'database/database.db')
    cursor = conn.cursor()

    keys_generated = 0
    while keys_generated < num_keys:
        key = generate_key()
        try:
            cursor.execute('''
                INSERT INTO licenses (license_key)
                VALUES (?)
            ''', (key,))
            conn.commit()
            print(f"Generated: {key}")
            keys_generated += 1
        except sqlite3.IntegrityError:
            # If key already exists, try again
            continue

    conn.close()


def get_user_input():
    """Get and validate user input for number of keys"""
    while True:
        try:
            num = int(input("Enter number of keys to generate (1-100): "))
            if 1 <= num <= 100:
                return num
            print("Please enter a number between 1 and 100")
        except ValueError:
            print("Invalid input. Please enter a number.")

def generator_main():
    create_database()
    num_keys = get_user_input()
    generate_keys(num_keys)
    print(f"\nSuccessfully generated {num_keys} license keys!")

generator_main()
