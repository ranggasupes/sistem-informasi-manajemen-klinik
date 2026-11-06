
from config.database import db

connection = db.connect()

if connection:
    print("Database klinik siap digunakan!")
    db.disconnect()
