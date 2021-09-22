# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:45:46 2021

@author: hrith
"""

from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime


UPLOAD_FOLDER = 'static/upload/'
app=Flask(__name__)
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
db=SQLAlchemy(app)
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    nm=db.Column(db.String(200),nullable=False)
    file=db.Column(db.LargeBinary)
    dt=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"


@app.route("/",methods=["GET","POST"]) 
def home():
    if request.method=="POST":
        return render_template("front.html")
    return render_template("front.html")

@app.route('/qutoes',methods=["GET","POST"])
def template():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        nm=request.form['nm']
        todo1=Todo(title=title,desc=desc,nm=nm)
        db.session.add(todo1)
        db.session.commit()
    alltodo=Todo.query.all()
    
    
    return render_template("index.html",alltodo=alltodo)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def updateit(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo1=Todo.query.filter_by(sno=sno).first()
        todo1.title=title
        todo1.desc=desc
        db.session.add(todo1)
        db.session.commit()
        return redirect("/qutoes")
    todo1=Todo.query.filter_by(sno=sno).first()
    
    return render_template('update1.html',todo1=todo1) 
   
@app.route("/delete/<int:sno>")
def delete(sno):
    todo1=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo1)
    db.session.commit()
    return redirect("/qutoes")
@app.route("/Story-teller",methods=['GET','POST'])
def show():
    if request.method=="POST":
        return render_template("td.html")
    return render_template("td.html")
@app.route("/about",methods=['GET','POST'])
def abo():
    if request.method=="POST":
        return render_template("about.html")
    return render_template("about.html")
@app.route("/movies",methods=["GET","POST"])
def com():
    if request.method=="POST":
        return render_template("commerce.html")
    return render_template("commerce.html")

if __name__=="__main__":
    app.run(debug=True,port=5000)
