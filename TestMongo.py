import pandas as pd
import pymongo

# pip install "pymongo[srv]" (Might be needed)

# Establishing the connectivity with the MangoDB atlas server
# URL of cloud
#
client = pymongo.MongoClient("mongodb+srv://dhan:******@cluster0.n0zji.mongodb.net/?retryWrites=true&w=majority")
db = client.test  # CALL THE CLIENT
# print(db)

#
# data = {
#     'name': 'DHANAN',
#     'email' : 'dh@gmail.com'
# }
#
# sample = client['Test']
# coll = sample['Sample1']
# coll.insert_one(data)


# attribute = pd.read_csv(r"C:\Users\preet\Desktop\DS\Data set\data fsds\Attribute DataSet.csv")
#
# # 4. Convert attribute dataset in json format
# att = attribute.fillna('NA')
# att = att.to_dict(orient='records')
#
# # 5. Store this dataset into mongodb
# # creating client
# client = pymongo.MongoClient('mongodb+srv://dhan:1212@cluster0.n0zji.mongodb.net/?retryWrites=true&w=majority')
# # connection to database
# db1 = client['Test']
# # creating collection
# coll = db1['attribute1271']
# coll.insert_many(att)
#
#
#

db1 = client['Test']
coll = db1['attribute1271']
datas = coll.find()

x = []
for data in datas:
    x.append(data)
x = pd.DataFrame(x)
x = x.drop(columns=['_id'], errors='ignore')
print(x)

