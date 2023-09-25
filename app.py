from flask import Flask
from flask import request
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
import firebase_admin
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


THIS_FOLDER = Path(__file__).parent.resolve()
my_file = THIS_FOLDER/"/service.json"
app = Flask(__name__)


cred =credentials.Certificate('service.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/custom",methods=["POST"])
def customToken():
    m_no=request.form['M_No']
    password=request.form['Password']
    doc_ref = db.collection("phone_pass").document(m_no)
    doc = doc_ref.get()
    if doc.exists:
        passs =  doc_ref.get(field_paths={'password'}).to_dict().get('password')
        if(passs==password):
            user_id = doc_ref.get(field_paths={'uid'}).to_dict().get('uid')
            custom_token = auth.create_custom_token(user_id)
            return custom_token
        else:
            return "true"
    else:
        return "false"


@app.route("/forget",methods=["POST"])
def forgot():
    m_no=request.form['M_No']
    doc_ref = db.collection("phone_pass").document(m_no)
    doc = doc_ref.get()
    if doc.exists:
        user_id = doc_ref.get(field_paths={'uid'}).to_dict().get('uid')
        custom_token = auth.create_custom_token(user_id)
        return custom_token
    else:
        return "false"

@app.route("/register",methods=["POST"])
def register():
    m_no=request.form['M_No']
    doc_ref = db.collection("phone_pass").document(m_no)
    doc = doc_ref.get()
    if doc.exists:
        return "true"
    else:
        return "false"
