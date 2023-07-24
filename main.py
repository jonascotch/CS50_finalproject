from flask import Flask, flash, redirect, render_template, request, session, url_for, g
import hashlib
import sqlalchemy
from sqlalchemy import create_engine, text
import sqlite3 as sql
from flask_session import Session
from helpers import login_required



app = Flask(__name__)

app.config['SECRET_KEY'] = "Your_secret_string"

# set session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# set the connection to the database
engine = sqlalchemy.create_engine('sqlite:///database.db')
db = engine.connect()

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        dbdata = db.execute(text('SELECT * FROM users')).fetchall()
        dbpass = dbdata[0].hash
        dbuser = dbdata[0].username        
        if dbpass == hashed_pw and username == dbuser:
            session['name'] = dbuser
            flash('Login correcto, ' + session['name'])
            return render_template('menu.html')
        else:
            flash('Tente de novo')
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['name'] = None
    flash('Logged out')
    return redirect('/')

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run(debug=True)