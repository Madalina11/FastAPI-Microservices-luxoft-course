from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import os

os.makedirs("data", exist_ok=True)

quest_db = TinyDB("data/questions.json", storage=CachingMiddleware(JSONStorage))
questions_table = quest_db.table("questions")
QuestionQuery = Query()