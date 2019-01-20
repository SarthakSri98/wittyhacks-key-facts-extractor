import pymongo
myclient = pymongo.MongoClient("mongodb://Sarthak:Sarthak98@ds161134.mlab.com:61134/wittyhacks")

mydb = myclient["wittyhacks"]
mycol = mydb["content"]

y={'topic':"text",'data': 'data_list'}
mycol.insert_one(y)

for x in mycol.find():
    print(x)

