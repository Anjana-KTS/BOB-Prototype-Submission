VIDEO LINKS PPT Description : https://drive.google.com/file/d/18DCLrwhKvU6WwxiFOJrhaG3J3BuYUPB2/view?usp=sharing

Azure Resources : https://drive.google.com/file/d/15b1_KsdFMtiEC0zsTH8IdadKiP-Z1CjT/view?usp=sharing

BOB DEMO VIDEO : https://drive.google.com/file/d/1lIDzpjfKA09ebep1RGrtXa1jLa4yYYlJ/view?usp=drivesdk

PPT https://docs.google.com/presentation/d/1lIS1VGty0XNZbe3b6MzoacpQlnr5kwfg/edit?usp=drivesdk&ouid=117347297960272883839&rtpof=true&sd=true

POC https://docs.google.com/document/d/1le6mlbhUFTg_vORixnN9-Fufm0vtzTT4/edit?usp=drivesdk&ouid=117347297960272883839&rtpof=true&sd=true

Setup

git clone https://github.com/ANUSHRUTHIKAE/BOB_PROJ.git

cd BOB_PROJ

pip install -r requirements.txt

download any one (32 bit or 64 bit)

from https://github.com/UB-Mannheim/tesseract/wiki

download mcr.traineddata into program files.

copy the path of tesseract.exe from Tesseract-OCR and paste in tess.pytesseract.tesseract_cmd = r" " in micr.py in BOB_PROJ

download (poppler-0.68.0_x86) from https://blog.alivate.com.au/poppler-windows/

and put in poppler_path = r"..........\poppler-0.68.0\bin"

python app.py

And test with

--> bob_bhuvana_signNV_1.jpg --> bob_kaaviya_nameNV_1.jpg --> BOB_pdf (2).pdf

DESCRIPTION
# BOB-Prototype-Submission
M-o-N-e-Y h-E-i-S-t
Bank handles large volumes of cheques in the clearing process. The process involves many technical verifications including signature verification. Some of these steps are manual and require human intervention to complete the process. The current process requires the high human capital deployment and longer processing time. Therefore this is high time to automate all the manual processes.


A website is created and this website will first ask the user to upload the image. This is done using a flask. 


Extraction

The form recognizer custom model is trained to extract the text from the cheques.
Sample cheque images are added and trained to recognize the fields.
The storage blob is connected to the form recognizer.
It will be connected using SAAS which will be generated every 6 hours. 
First, the form recognizer will extract all the words. Then we have to create a tag and label the fields. 
This process is to be repeated and train the model. An endpoint is given to the form recognizer.


After uploading, all the extracted details will be displayed.
Extraction is done in JSON.





IFSC Extraction
IFSC code consists of four alphabets denoting the bank.
The fifth will be zero.
From the Sixth it will be alphanumeric denoting the branch.
Razorpay API is connected. The extracted code is verified using the API.
It will verify and validate the bank name and branch name with the extracted IFSC code.




 MICR Extraction
Magnetic Ink Character Recognition (MICR) is a 9-digit code that helps identify a particular bank branch that is part of the Electronic Clearing System (ECS)
A self-trained model is used to predict the MICR code.
When MICR is parsed it has delimiters at the end of every part, these delimiters are read as alphabets A or C.
It will return the MICR line in raw format as a string, with delimiters to separate the account number, routing number, and check number.



 Type of Account
All the types of accounts are given in a list.

* The different types of bank accounts are – Savings Accounts, Current Accounts,     Recurring Deposit Accounts, Fixed Deposit Accounts, DEMAT Accounts, and NRI accounts.

The output extracted from the form recognizer should match the account type list. 
Verification is done.


 Account Number Verification
An account number is a set of digits used to identify a bank account

This verification is split into two parts :
First, we have to verify whether it is in a valid format or not.
 * Account number has 11 to 17 numbers in general.
 * A connection to CosmoDB is made.
 * CosmoDB consists of documents with account details.
 * An SMS is sent to the number.
 * Secret code is also present in the DB.
 * Every signature has an ID. this ID will let us know whose sign to check.
 
The minimum balance is also checked.
The cheque number must be from 0 to 10 or else it is false.




 Payee and account holder verification
Payee: The person named in the cheque who is to receive the payment. 
Drawer: The person who writes the cheque, who can be the account holder or the customer. 

A function is used to verify Payee and Accountholder
For payee
* Name is verified.

For Account holder
* Account Number is verified.
The process Will further continue only if the name and account number are available.

Any local branch is applicable if the cheque has transaction codes 9 10 11.

Any bank is applicable if the cheque has transaction codes 29 30 31.




Date Verification
The date is compared with the date given in the database.
The Extracted Date must be less than the one given in the database.




 Amount Verification
The legal amount and courtesy amount:

The amount written in words is called the ‘legal amount’ of the cheque and the amount written in figures is called the ‘courtesy amount’. Where there is a difference between words and figures expressed in a cheque, the amount in words is the amount payable as per Section 18 of N.I.Act 1881. It is customary to return a cheque written only in figures with the reason “Amount required in words”. However, if the amount is written only in words, though it is unusual in form, it is not incomplete and therefore bank must pay the cheque, lest they would probably be liable to their customer for any damage or loss incurred through refusal.


Texts are converted to numbers using text2int.
The legal amount and the courtesy amount must be the same.

 Account Balance
The Account's main balance minus the legal amount must be greater than zero. 


 Cheque Number Verification
Every cheque leaf has a 6-digit cheque number written at the bottom left-hand side of the cheque.
The cheque is valid if the cheque number is from 0 to 20.


Complete Verification
Two cases are possible 
 * All are verified then proceed to signature verification.
 * Some are not verified then show invalid.

Signature verification will denote the success of all the previous verification cases.



 Signature verification
It consists of three cases

*The sign ID is sent to signverify.py
*Feature mapping is the concept used to verify signatures.
*The Features of a signature are converted into an array.
*Eccentricity, Center from x, Center from y, Solidity, Ratio, skew lines from x and y, and kurtosis from x and y are the features.

Eccentricity-Deviation of a curve or orbit from circularity.

Kurtosis-A measure of the tailedness of a distribution.

Skew lines- A pair of lines that are non-intersecting, non-parallel, and non-coplanar.

Solidity- The quality or state of being solid.

*CSV file is used to store the features.
*Functions are used to extract the features.
*Cropsign is used to crop where the signature is present.
*Form recognizer sets up boundary box.
*The signature ID and Image cropped are compared.
*The cropped image will be saved.


In the end, OTP is sent to the number and the secret code is to be entered to complete the transaction.
