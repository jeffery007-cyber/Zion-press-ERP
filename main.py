from database.db import Database
from modules.login import LoginWindow

db = Database()
db.create_tables()
db.close()

LoginWindow()