import pygame
import shared
import sqlite3
import bcrypt

# REMOVE ALL USERDATA
conn = sqlite3.connect(shared.path + 'database/database.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM users')
conn.commit()