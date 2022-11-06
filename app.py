
#import all the required dependencies

from flask import Flask, render_template,flash,redirect,url_for,request,session
from werkzeug.utils import secure_filename
import os
from CompleteVerify import CompleteVerify
from Transaction import Transaction
from pdfimgcon import pdf
from os import listdir
app=Flask(__name__)
# folder path




app.config['SECRET_KEY']='cairocoders-ednalan'

UPLOAD_FOLDER=os.path.join('static', 'uploads')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024


ALLOWED_EXTENSIONS= set(['pdf','png','jpg','jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    global img_file_path
    img_file_path = session.get('uploaded_img_file_path', None)

    global Extracted
    global Verified
    global Status
    Extracted=CompleteVerify(img_file_path)
    global secret_pin
    global OTP
    if(len(Extracted)>3):
            secret_pin=Extracted[2]
        
            OTP=Extracted[5]
    Verified=Extracted[0]
    Status=Extracted[1]
    

    
    if(Status == 'Verified'):
        
        
        # Display image in Flask application web page
        return render_template('view2.html', user_image = img_file_path,Verified=Verified,Status=Status,format=format,path=img_file_path)
    else:
        return render_template('view2.html', user_image = img_file_path,Verified=Verified,Status=Status,path=img_file_path,format=format)
    
            
@app.route('/otpform',methods=['POST'])
def otpform():
    if request.method == "POST" :

        Secret_pin_user= request.form.get("spin")
        OTP_user= request.form.get("OTP")
        print(secret_pin)
        string="Transaction Not Verified"
        print(Secret_pin_user,secret_pin)
        if str(Secret_pin_user)==str(secret_pin):
            print(OTP_user,OTP)
            if int(OTP_user) == int(OTP):
                # Transaction(Extracted[3],Extracted[4],Extracted[6],Extracted[7],Verified['Legal Amount'])
                string="TRANSACTION COMPLETE"
        print(string)
        if format=='image':
            return render_template('viewotp.html', user_image = img_file_path,Verified=Verified,Status=Status,String=string,format=format)
        else:
            return render_template('viewotp.html', user_image = path,Verified=Verified,Status=Status,String=string,format=format,ind=session.get('ind123'))

@app.route('/pdf2')
def pdf2():

    session['ind123']=0
    pdf(session.get('uploaded_img_file_path', None))
    dir_path = r'static\uploads\Chequeimages'
    length = 0
    # Iterate directory
    for path1 in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path1)):
            length += 1
    print('File count:', length)
    session['length']=length
    return redirect('/viewpdf1')

@app.route('/viewpdf1')
def viewpdf1():

   
    ind123=session.get('ind123')
    length=session.get('length')
    if(ind123 < length):
        global path
        path='static/uploads/Chequeimages/page'+ str(ind123) +'.png'
        
        val =ind123+1
        ind123=val

        global Extracted
        global Verified
        global Status
        Extracted=CompleteVerify(path)
        global secret_pin
        global OTP
        if(len(Extracted)>3):
            secret_pin=Extracted[2]
        
            OTP=Extracted[5]
        Verified=Extracted[0]
        Status=Extracted[1]        
        session['ind123']=ind123
        print(ind123,"ysuaddddddd")
        if(Status == 'Verified'):
            
            Verified=Extracted[0]
            Status=Extracted[1]
            secret_pin=Extracted[2]
            OTP=Extracted[5]

            # Display image in Flask application web page
            return render_template('view2.html', user_image = path,Verified=Verified,Status=Status,path=path,format=format)
        else:
            print(format)
            return render_template('view2.html', user_image = path,Verified=Verified,Status=Status,path=path,format=format)
    else:
        redirect('/') 

@app.route('/upload',methods=['POST'])
def upload():
    file= request.files['inputfile']
    filename = secure_filename(file.filename)
    
    if file and allowed_file(file.filename):
        global format
        
        # #pdf format
        if('.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'):
            format='pdf'
            
            # Chequeimages
            filename="import.pdf"
            file.save(os.path.join('static\\uploads', filename))
            session['uploaded_img_file_path'] = os.path.join('static\\uploads', filename)
            return redirect('/pdf2')
        #jpg,jpeg and png
        else:
            format='image'
            filename="import.jpg"
            file.save(os.path.join('static\\uploads', filename))
            session['uploaded_img_file_path'] = os.path.join('static\\uploads', filename)
            return redirect('/view')

    else:
        flash('Invalid Upload only pdf,png,jpg,jpeg')
        # return redirect('/')
    return redirect('/') 

    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)