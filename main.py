from flask import Flask, flash, redirect, render_template, request, session, url_for, g
import hashlib
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
def sql_open():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cursor = con.cursor()

    return cursor

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        cursor = sql_open()
        cursor.execute('SELECT username, hash FROM users')
        userdata = cursor.fetchone()
        cursor.close()
        if userdata['hash'] == hashed_pw and userdata['username'] == username:
            session['name'] = username
            flash('Welcome, ' + session['name'])
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

@app.route('/newform', methods=('GET', 'POST'))
def newform():
    return render_template('newform.html')

if __name__ == "__main__":
    app.run(debug=True)