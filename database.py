from pymongo import MongoClient, ASCENDING, DESCENDING
from dotenv import load_dotenv
import os

load_dotenv(".env")
username = os.getenv("username")
password = os.getenv("password")

client = MongoClient(f"mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed08"]  # use <database_name>
collection = db["thanida_enrollment_system"]  # db.collection_name


# collection.insert_one({'person': '1'})

# collection.insert_many(
#     [
        # {"std_id": 1, "std_name": "junior", "course_name": "Digit", "grade": 3, "unit": 3},
        # {"std_id": 1, "std_name": "junior", "course_name": "Math III", "grade": 4, "unit": 3}
        # {"std_id": 2, "std_name": "grizzly", "course_name": "Computer Network", "grade": 3, "unit": 3},
        # {"std_id": 3, "std_name": "Peter", "course_name": "Data & Algo", "grade": 3, "unit": 3},
        # {"std_id": 4, "std_name": "Taylor", "course_name": "Computer system", "grade": 1, "unit": 3},
        # {"std_id": 5, "std_name": "Charlie", "course_name": "KE & KM", "grade": 2, "unit": 3}
#     ]
# )

# collection.update_many([{"std_id": 1}, {"std_id": 2}], {"$set": {"grade": 4}})

# collection.delete_one({'course_name': 'Computer system'})

print(db.list_collection_names())

origin_data = collection.find()

for i in origin_data:
    print(i)