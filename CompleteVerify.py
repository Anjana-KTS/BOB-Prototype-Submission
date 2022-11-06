from ExtractVerify import ExtractVerify
from cropsignature import cropsign
from Signverify import signverify

# !pip install twilio
from twilio.rest import Client

from random import randint
def OTP_verification(phone):
    OTP = randint(10**5, 10**6-1)
    print(OTP)
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure

    #uncommment

    account_sid = 'ACb9240d5ce231ddd455edd369cc6b52c9'
    auth_token ='1d00eda7351b7f6ec25162d007a50890'
    # Phone_number="+91"+str(Account_holder_phone_no)
    Phone_number="+91"+str(phone)
    client = Client(account_sid, auth_token)
    Message_OTP="Your Cheque is verified .Your OTP is"+str(OTP)
    message = client.messages \
                    .create(
                        body=Message_OTP,
                        from_='+14245443593',
                        to=Phone_number)
    return OTP

def CompleteVerify(path):
    Extracted = ExtractVerify(path)
    Verified=Extracted[0]
    Status=Extracted[1]

    if(Extracted[1]=='VERIFIED'):
        
        cropsign(path,Extracted[2])
        if signverify('013') == 'Genuine Image':
            Verified['Signature']="Genuine"
            phone=Extracted[5]
            print(phone)
            OTP=OTP_verification(phone)
            #return Verified json status AccountHolderid Payee id
            return Verified,Status,Extracted[4],Extracted[6],Extracted[7],OTP,Extracted[8],Extracted[9]
        else:
            return "SIGNATURE NOT VERIFIED","NOT VERIFIED"
    else:
        return Verified,Status
# Transaction(r'page0.png')
# CompleteVerify('static/uploads/Chequeimages/page'+ str(0) +'.png')