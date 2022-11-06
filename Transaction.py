import pymongo
myclient =pymongo.MongoClient("mongodb://verification:5l6oSsIxDhTx9d3TBT0MIOcDbGDG0jD5x0r5jxD0OirGI3jGGKnpkWgNQXpF1fTXK0xZECJHuTpNBCWl2I1cDw==@verification.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@verification@")

mydb=myclient["hrdb"]
mycol=mydb["Account_database"]
def Transaction(A_id,P_id,Balance,payee_Balance,AMOUNT):

    mycol.update_one({"_id":A_id},{"$set":{"Balance":Balance+AMOUNT}})
    mycol.update_one({"_id":P_id},{"$set":{"Balance":payee_Balance-AMOUNT}})
    print("Transaction Complete")