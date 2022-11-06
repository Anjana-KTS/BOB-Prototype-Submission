import pymongo
myclient =pymongo.MongoClient("mongodb://verification:5l6oSsIxDhTx9d3TBT0MIOcDbGDG0jD5x0r5jxD0OirGI3jGGKnpkWgNQXpF1fTXK0xZECJHuTpNBCWl2I1cDw==@verification.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@verification@")

mydb=myclient["hrdb"]
mycol=mydb["Account_database"]

num=7397429454
# insert the record
Account_database1={
    'IFSC_code': 'BARB0KODAMB', 
 'Account_Number': '29870690112931', 
 'Account_holder_Name': 'ANU', 
 'Phone_Number': num, 
 'Balance': 50000, 
 'Cheque_Number_alloted_from': '000071', 
 'Cheque_Number_alloted_to': '000080', 
 'Till_date': '11-04-2022',
 'Sign_ID': '012',
  'Secret_PIN':"0002"
}
Account_database2={
    "IFSC_code":"BARB0KODAMB",
    "Account_Number":"19870690112932",
    "Account_holder_Name":"KAAVIYA",
    "Phone_Number":num,
    "Balance":50000,
    "Cheque_Number_alloted_from":"000021",
    "Cheque_Number_alloted_to":"000040",
    "Till_date":"11-04-2022",
    "Sign_ID":"011",
    'Secret_PIN':"0001"
}
Account_database3={
  'IFSC_code': 'BARB0KODAMB',
  'Account_Number': '49510100002748',
  'Account_holder_Name': 'ASHWATH G SINDHUJA P',
  'Phone_Number': num,
  'Balance': 1000000,
  'Cheque_Number_alloted_from': '000000',
  'Cheque_Number_alloted_to': '000020',
  'Till_date': '23-02-2022',
  'Sign_ID': '013',
  'Secret_PIN':"0000"
}
Account_database4= {'IFSC_code': 'BARB0KODAMB', 
 'Account_Number': '49870690112933', 
 'Account_holder_Name': 'Bhuvana', 
 'Phone_Number': num, 
 'Balance': 50000, 
 'Cheque_Number_alloted_from': '000041', 
 'Cheque_Number_alloted_to': '000060', 
 'Till_date': '11-04-2022', 
 'Sign_ID': '010',
'Secret_PIN':"0003"}
Account_database5= {'IFSC_code': 'BARB0KODAMB', 
 'Account_Number': '59870690112935', 
 'Account_holder_Name': 'EZHIL', 
 'Phone_Number': num, 
 'Balance': 50000, 
 'Cheque_Number_alloted_from': '000081', 
 'Cheque_Number_alloted_to': '000100', 
 'Till_date': '11-04-2022', 
 'Sign_ID': '009',
'Secret_PIN':"0004"}
Account_database6= {'IFSC_code': 'BARB0KODAMB', 
 'Account_Number': '69870690112936', 
 'Account_holder_Name': 'Ashik', 
 'Phone_Number': num, 
 'Balance': 50000, 
 'Cheque_Number_alloted_from': '000101', 
 'Cheque_Number_alloted_to': '000120', 
 'Till_date': '11-04-2022', 
 'Sign_ID': '008',
'Secret_PIN':"0005"}


mycol.insert_one(Account_database1)
mycol.insert_one(Account_database2)
mycol.insert_one(Account_database3)
mycol.insert_one(Account_database4)
mycol.insert_one(Account_database5)
mycol.insert_one(Account_database6)