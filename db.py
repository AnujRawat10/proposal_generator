from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import certifi

# Use clean base URI — no query params
MONGO_URI = "mongodb+srv://anujrawat9639:Y2noc8qlyZbYOVyG@cluster0.k0bt7en.mongodb.net"

# Use certifi for SSL verification (required on Streamlit Cloud)
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())

db = client["proposalgenerator"]
collection = db["proposals"]

def save_proposal(proposal_text, client_name, domain):
    doc = {
        "client": client_name,
        "domain": domain,
        "content": proposal_text,
        "created_at": datetime.datetime.utcnow()
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_proposal_by_id(proposal_id):
    try:
        doc = collection.find_one({"_id": ObjectId(proposal_id)})
        return doc.get("content") if doc else None
    except:
        return None
