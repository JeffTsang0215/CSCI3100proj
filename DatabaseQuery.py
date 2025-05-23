'''
DEVELOPER'S KIT
'''


import pygame
import shared
import sqlite3
import bcrypt



conn = sqlite3.connect(shared.path + 'database/database.db')
cursor = conn.cursor()

# # REMOVE ALL USERDATA
# cursor.execute('DELETE FROM users')
# conn.commit()

# Drop the existing table
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS user_card_collection')
cursor.execute('DROP TABLE IF EXISTS user_progress')

# Create table with new schema
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY UNIQUE,
                 password TEXT NOT NULL,
                 security_question1 TEXT NOT NULL,
                 security_answer1 TEXT NOT NULL,
                 security_question2 TEXT NOT NULL,
                 security_answer2 TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_card_collection
                (username TEXT PRIMARY KEY UNIQUE,
                 unlock_cards TEXT NOT NULL,
                 decks TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_progress
                (username TEXT PRIMARY KEY UNIQUE,
                 gold INT NOT NULL,
                 battle_record TEXT NOT NULL)''')
conn.commit()
conn.close()