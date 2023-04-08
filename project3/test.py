from flask import Flask,render_template,request
import openai
from speech_recognition import *
from pyttsx3 import *

e=init()

l=Recognizer() 

openai.api_key="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"


app = Flask(__name__)

@app.route("/")
def hello():
    
    return render_template('home.html')

@app.route("/",methods=['POST'])
def new():
    # name=request.form['name']
    with Microphone() as source:
        v=l.listen(source)
        data=l.recognize_google(v)
        model="text-curie-001"
        c=openai.Completion.create(model= "text-davinci-003",prompt= data,max_tokens= 1024,temperature= 0.5,top_p= 1,n= 1,stop=None)
        r=c.choices[0].text
       

    return render_template('home.html',name1=r)

app.run()