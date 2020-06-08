import json, os, sys
from pymongo import MongoClient

mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

# Choose InfoSys database
db = client['InfoSys']
movies = db['Movies']
users = db['Users']

def insertuser(entry):
    try:
        users.insert_one(entry)
        return True 
    except Exception as e:
        print(e)
        return False 
        
def insertmovie(entry):
    try:
        movies.insert_one(entry)
        return True 
    except Exception as e:
        print(e)
        return False 

def insert_all_users():
    file = open('./data/users.json','r')
    lines = file.readlines()
    for line in lines:
        entry = None 
        try:
            entry = json.loads(line)
        except Exception as e:
            print(e)
            continue
        if entry != None:
            entry.pop("_id",None) 
            insertuser(entry)

def insert_all_movies():
    file = open('./data/movies.json','r')
    lines = file.readlines()
    for line in lines:
        entry = None 
        try:
            entry = json.loads(line)
        except Exception as e:
            print(e)
            continue
        if entry != None:
            entry.pop("_id",None) 
            year = entry["year"]
            rating = entry["rating"]
            totalratings = entry["totalratings"]
            entry["totalratings"] = int(totalratings)
            entry["rating"] = float(rating)
            entry["year"] = int(year) 
            if "ratings" in entry:
                ratings = entry["ratings"]
                n_ratings = []
                for rt in ratings:
                    rate = rt["rate"]
                    rt["rate"] = float(rate)
                    n_ratings.append(rt)
            entry ["ratings"] = n_ratings
            insertmovie(entry)

def insert_all():
    insert_all_users()
    insert_all_movies()
    print("Insertion completed")