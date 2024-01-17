from pymongo import MongoClient
from constants.bot_config import MONGODB_PASS


async def get_data(document_id, database, collection):
    cluster = MongoClient(f"mongodb+srv://Seazyns:{MONGODB_PASS}@skyblockbot.ghy78.mongodb.net/skybot?retryWrites=true&w=majority")
    data = cluster[f"{database}"][f"{collection}"].find_one({"_id": document_id})
    return data


async def store_data(document_id, data, database, collection):
    cluster = MongoClient(f"mongodb+srv://Seazyns:{MONGODB_PASS}@skyblockbot.ghy78.mongodb.net/skybot?retryWrites=true&w=majority")
    cluster[f"{database}"][f"{collection}"].update_one({"_id": document_id}, {"$set": data})


async def create_data(data, database, collection):
    cluster = MongoClient(f"mongodb+srv://Seazyns:{MONGODB_PASS}@skyblockbot.ghy78.mongodb.net/skybot?retryWrites=true&w=majority")
    cluster[f"{database}"][f"{collection}"].insert_one(data)
