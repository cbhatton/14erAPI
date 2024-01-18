import json
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")

db = client["colorado14ers"]
collection = db["peaks"]

# with open('colorado-14ers.json', 'r') as f:
#   peaks = json.load(f)
#
# for name, peak in peaks.items():
#   # set id the peak key
#   peak['_id'] = name
#   collection.insert_one(peak)


posts = db.posts
# post_id = posts.insert_one(post).inserted_id

n = 0
for c in collection.find():
  print(c)
  n += 1

print(n)