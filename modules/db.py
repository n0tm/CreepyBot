from pymongo import MongoClient

client = MongoClient()
db = client['CreepyBot']
print("\nСоединение с Базой данных установленно...")
print(db.phrases.find_one())