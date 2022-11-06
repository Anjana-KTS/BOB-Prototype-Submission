import requests
import json
import time
from requests import get, post


from micr import micr
import pymongo

def ExtractVerify(path):
    endpoint= "https://chequeformrecogniser.cognitiveservices.azure.com/"
    key="334ca57eb69f494e9700ee69324e5b4d"
    model_id="01175162-b65b-4c0a-9b1b-2e8b4fbf73fa" 
    post_at= endpoint +"/formrecognizer/v2.0/custom/models/%s/analyze" % model_id
    f=open(path,"rb")
    headers={
    'Content-Type' : 'image/jpeg',
    'Ocp-Apim-Subscription-Key' : key,
    }
    cheque_number,final_micr,Account_ID,Transaction_code=micr(path)
    try:
        response= post(url=post_at,data=f.read(),headers= headers)
        if response.status_code == 202:
            print("POST operation successful")
        else:
            print("Post operation failed: \n%s" % json.dumps(response.json()))
            quit()
        get_url=response.headers["operation-location"]
    except Exception as ex:
        print("Exception details:%s"% str(ex))
        quit()
    time.sleep(10)
    response = get(url = get_url , headers= {"Ocp-Apim-Subscription-Key": key})
    json_response = response.json()
    if response.status_code != 200:
        print("GET operation failed:\n%s" %json.dumps(json_response))
        quit()
    status = json_response["status"]
    print("Code Status : ",status)

    #*****************************Extraction of Cheque Details from String****************************

    ex=json_response['analyzeResult']['documentResults'][0]['fields']
    print(ex.keys())
    json={}
    for key,val in ex.items():
    
        if key == 'Signature':
            signbound=val['boundingBox']
            sign_bound_tuple=int(signbound[1]),int(signbound[5]),int(signbound[0]),int(signbound[2])
            json[key] = sign_bound_tuple
        else:
            json[key] = val['text']
    print(json)

    Verified={}
    
    def IFSC(IFSC):
        ''' 
        Extract IFSC (Indian Financial System Code)

        The IFSC is an 11 digit alpha numeric code with :

        1. The first four digits identifying the bank
        2. fifth is numeric (kept 0) 
        3. The last six digits represent the bank branch. 

        '''
        if IFSC!=None and IFSC[:4].isalpha and IFSC[5:].isalnum() :
            #  5th digit is 0 
            Verified['IFSC']=IFSC[:4]+'0'+IFSC[5:]
            print("IFSC Verified :",Verified['IFSC'])
            return Verified['IFSC']
        else:
            print("IFSC Not Verified!")
            return None
    IFSC=IFSC(json['IFSC'])
    
    if IFSC == None:

        return "IFSC NOT VERIFIED!","NOT VERIFIED"
    
    '''Getting the Bank Name and Branch Name and MICR 
    via Razorpay API using the IFSC and Verifying it with the extracted String'''

    data = requests.get("https://ifsc.razorpay.com/"+IFSC).json()

    def Bank_Name(api,BankName):
        #Find Bank Name from API in Extracted Bank Name
        if(api["BANK"] in BankName):
            Verified['Bank Name']=api["BANK"]
            print("Bank Name Verified:", Verified["Bank Name"])
            return 0
        else:
            print("Bank Name Not Verfied")
            return 1
            
    if Bank_Name(data,json['BankName']):
        return "BANK NAME NOT VERIFIED!","NOT VERIFIED"
    
    def Branch_Name(api,BranchName):

    #Find Branch Name from API in Extracted Branch Name
    #Sometimes the Branch Name given in the API is a comma-seperated value.
    #thus we compare the presence of value before the comma with the Branch Name

        if(api["BRANCH"].upper() in BranchName.upper() or api["BRANCH"].split(',')[0].upper() in BranchName.upper()):
            Verified['Branch Name']=api["BRANCH"]
            print("Branch Name Verified:", Verified["Branch Name"])
            return 0
        else:
            print("Branch Name Not Verfied")
            return 1
    
    if Branch_Name(data,json['BranchName']):
        return "BRANCH NAME NOT VERIFIED!","NOT VERIFIED"

    # final_micr="600012059"

    def MICR(api,micr):
        if(api["MICR"] ==micr):
            Verified['MICR']=api["MICR"]
            print("MICR Verified:", Verified["MICR"])
            return 0
        else:
            print("MICR Not Verfied",micr," asd")
            return 1
    if MICR(data,final_micr):
        return "MICR NOT VERIFIED!","NOT VERIFIED"
    

    '''
    Extracting the Type of Account

    1. CURRENT ACCOUNT
    2. SAVINGS ACCOUNT
    3. SALARY ACCOUNT
    4. FIXED DEPOSIT ACCOUNTS
    5. RECURRING DEPOSIT ACCOUNTS 
    6. NRI ACCOUNT
    '''

    def Type_of_Account(Acc_Type):
        Types_of_Account=['CURRENT ACCOUNT','SAVINGS ACCOUNT','SALARY ACCOUNT','FIXED DEPOSIT ACCOUNTS','RECURRING DEPOSIT ACCOUNTS','NRI ACCOUNT']
        flag=0
        for ind_type,val_type in enumerate(Types_of_Account):
            if val_type in Acc_Type:
                Verified['Type of Account']=Types_of_Account[ind_type]
                print("Type of Account Verified:", Verified['Type of Account'])
                return 1
        print("Type of Account Not Verfied")
        return "TYPE OF ACCOUNT NOT VERFIED!","NOT VERIFIED"
    Type_of_Account(json['Type of Account'])

    '''Account Number

    In India, public sector banks have their pattern and usually follow an 11 digit pattern. 
    However, private sector banks use either a 12 digit account or a 14 digit account number 
    and can be upto 17 digits long.'''

    def Acc_No_Format(AccNo):
        if len(AccNo) in range(11,18) and AccNo.isdigit() :
            return AccNo
        else:
            print("Account Number - Format Not verified")
            return 0
     
    Account_Number_informat=Acc_No_Format(json['AccountNumber'])
    if not(Account_Number_informat) :
        return "ACCOUNT NUMBER NOT VERIFIED","NOT VERIFIED"

    myclient =pymongo.MongoClient("mongodb://verification:5l6oSsIxDhTx9d3TBT0MIOcDbGDG0jD5x0r5jxD0OirGI3jGGKnpkWgNQXpF1fTXK0xZECJHuTpNBCWl2I1cDw==@verification.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@verification@")

    mydb=myclient["hrdb"]
    mycol=mydb["Account_database"]

    '''Get Details from the Database for Payee and Account Holder'''

    
    def DatabaseINFO_Account_Holder(json,Account_Number):
        for record in mycol.find():
            if record['Account_Number']== Account_Number  :
                return record
        return 0
    def DatabaseINFO_Payee(json,Account_Number):
        for record in mycol.find():
            if record['Account_holder_Name'] in json['Payee']: 
                return record
        return 0


    Account_Holder_details = DatabaseINFO_Account_Holder(json,Account_Number_informat)

    
    
    '''Account Number Verification

    To check wether the Account Number is present in the database'''  

    if not(Account_Holder_details):
        return "ACCOUNT NUMBER NOT IN DATABASE!","NOT VERIFIED"
    else:
        Verified['Account Number']=Account_Number_informat
        print("Account Number Verified:", Verified["Account Number"])
    
    
    payee_details= DatabaseINFO_Payee(json,Account_Number_informat)

    '''Payee Verification

    To check whether the payee is present in the Database'''
    
    if not(payee_details):
        return "PAYEE NOT IN DATABASE!","NOT VERIFIED"
    else:
        Verified['Payee']=payee_details['Account_holder_Name']
        print("Payee Verified:", Verified['Payee'])
    
    '''Date Verification

    To verify that the Date given in the cheque is Before the deadline for the expiry of cheque.'''

    def date_verify(date,till_date):
    
        #format: from :DD-MM-YYYY
        #format: change to : DDMMYYYY
        
        till_date = till_date.replace("-","")
        date=date.replace("-","")
        #YYYY
        if int(date[4:8])== int(till_date[4:8]):
            #MM
            if int(date[2:4] == till_date[2:4]):
            #DD
                if int(date[0:2] <= till_date[0:2]):
                    return 1
            elif int(date[2:4] <= till_date[2:4]):
                return 1
        elif int(date[4:8])<= int(till_date[4:8]):
            return 1
        return 0
    date=json['Date'].replace(" ", "")
    date=date[0:2]+'-'+date[2:4]+'-'+date[4:8]

    if date_verify(date,Account_Holder_details['Till_date']):
        
        Verified['Date']=str(date)
        print("Date Verified:", Verified["Date"])
    else:
        print("Date Not Verfied")
        return 'Date'+str(date)+'Applicable only till'+str(Account_Holder_details['Till_date'])+"!","NOT VERIFIED"
    

    '''Amount Verification

    To Verify whether the legal and courtesy amount are same.'''

    def text2int(textnum, numwords={}):
        if not numwords:
            units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):    
                numwords[word] = (1, idx)
            for idx, word in enumerate(tens):     
                numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales):   
                numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        words=""
        for word in textnum.split():
            if word not in numwords:
                # raise Exception("Illegal word: " + word)
                pass
            if word in numwords:
                words+=word.title()+" "
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0

        return result + current,words
    
    Legal_Amount,Courtesy_Amount=text2int(json['CourtesyAmount'].lower())
    
    if(Legal_Amount==int(json['LegalAmount'])):
        Verified['Courtesy Amount']= Courtesy_Amount 
        Verified['Legal Amount'] = json['LegalAmount']
        print("Amount Verified:", Verified["Courtesy Amount"],"(",Verified["Legal Amount"],")")
    else:
        print("Amount not Verified")
        return "AMOUNT NOT VERIFIED","NOT VERIFIED"
    

    
    '''Balance Verification

    We verify that the Balance of Account holder is feasible for transactions 
    and check whether the balance after transaction is greater than the minimum balance.
    '''
    Required_min_balance = 0
    if Account_Holder_details['Balance']-Legal_Amount > Required_min_balance :
        Verified['Balance (Before transaction)']=str(Account_Holder_details['Balance'])
        print("Verified Balance (Before transaction) :", Verified["Balance (Before transaction)"])
    else:
        print("Balance Not Verfied")
        return "NO ENOUGH BALANCE!","NOT VERIFIED"

    
    
    '''Cheque Number Verification

    We verify the Cheque Number to be between the allocated numbers from the database.
    '''

    if int(cheque_number) >= int(Account_Holder_details['Cheque_Number_alloted_from']) and int(cheque_number) <= int(Account_Holder_details['Cheque_Number_alloted_to']):
        Verified['Cheque Number']=cheque_number
        print("Verified Cheque Number:", Verified["Cheque Number"])
    else:
        print("Cheque Number Not Verified",cheque_number,Transaction_code,Account_ID)
        return "CHEQUE NUMBER NOT VERIFIED!","NOT VERIFIED"

    
    return Verified,"VERIFIED",json['Signature'],Account_Holder_details['Sign_ID'],Account_Holder_details['Secret_PIN'],Account_Holder_details['Phone_Number'],Account_Holder_details['_id'],payee_details['_id'],Account_Holder_details['Balance'],payee_details['Balance']
# path=r'page0.png' 
# print(ExtractVerify(path))
