from flask import Flask, flash, redirect, render_template, request, session, url_for, json
import hashlib
import sqlite3 as sql
from flask_session import Session
from helpers import login_required
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "This is a really g00d secret keY!"

# set session
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# set the connection to the database
def sql_open():
    con = sql.connect('database.db')
    con.row_factory = sql.Row

    return con

# base route
@app.route('/')
def root():
    con = sql_open()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ruts WHERE public=? AND solved = ?", ('true', 'false'))
    data = cursor.fetchall()
    cursor.close()
    return render_template('landing.html', data=data)

# route for logging in
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # get input from user
        username = request.form.get('username')
        password = request.form.get('password')
        # get hash from inputed password
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        # get data from db
        con = sql_open()
        cursor = con.cursor()
        cursor.execute('SELECT username, hash FROM users')
        userdata = cursor.fetchone()
        cursor.close()

        # if inputed data checks with db, render menu
        if userdata['hash'] == hashed_pw and userdata['username'] == username:
            session['name'] = username
            flash('Welcome, ' + session['name'])
            return render_template('menu.html')
        
        # else, return to login
        else:
            flash('Tente de novo')
            return redirect('/login')
    # if request is no POST typr, return to login
    else:
        return render_template('login.html')

# route for logging out
@app.route('/logout')
def logout():
    # clear session and return to base route
    session['name'] = None
    flash('Logged out')
    return redirect('/')

# route for app menu
@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

# route to insert new data
@app.route('/newform', methods=('GET', 'POST'))
def newform():
    # if request method is POST
    if request.method =='POST':
        # get data from form
        data = request.form   
        # manage some trouble data (checkboxes)     
        try:
            public = data['public']
        except:
            public = 'false'
        try:
            solved = data['solved']
        except:
            solved = 'false'
        
        # generate created timestamp
        now = datetime.now()
        created = now.strftime("%Y-%m-%d %H:%M:%S")

        # open db connection and insert data
        con = sql_open()
        con.execute("INSERT INTO ruts (code, desig, forn, order_nr, end_date, last_date, alternative, detail, obs, created, public, solved) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (data['code'], data['desig'], data['forn'], data['order'], data['enddate'],data['lastdate'], data['alter'], data['detail'], data['obs'], created, public, solved))
        con.commit()
        con.close()

        #confirm data entry and render app menu
        flash('Registo inserido com sucesso')
        return render_template('menu.html')
    
    # if not post, return to form
    return render_template('newform.html')

# route to get list of data in database, 3 types of list according to user selection in menu the status is passed to the function
@app.route('/list/<status>', methods=['GET'])
@login_required
def list(status):
    # open db connection
    con = sql_open()
    cursor = con.cursor()

    # unsolved shortages
    if status == 'other':
        cursor.execute("SELECT * FROM ruts WHERE solved = ?", ('false',))
        list_Type = '(por resolver)'        
    
    # public data
    elif status == 'public':
        cursor.execute("SELECT * FROM ruts WHERE public = ?", ('true', ))
        list_Type = '(públicas)'
    
    # all data
    else:
        cursor.execute("SELECT * FROM ruts")
        list_Type = '(todas)'

    # assign fetched data to variable and pass it to list template    
    data = cursor.fetchall()
    cursor.close()
    return render_template('list.html', data=data, listType=list_Type)

# route to see all details from db entry, the id is passed to the function
@app.route('/details/<id>')
@login_required
def details(id):
    # open db connection and get data according to passed id
    con = sql_open()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ruts WHERE id=?", (id,))
    data = cursor.fetchone()
    # render data on details template
    return render_template('details.html', data=data)

# route to edit data entry
@app.route('/edit/<id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    # if changes are submitted
    if request.method == 'POST':
        # get data from form
        data = request.form

        # manage checkboxes        
        try:
            public = data['public']
        except:
            public = 'false'
        try:
            solved = data['solved']
        except:
            solved = 'false'
        
        # open db connection and update data entrt
        con = sql_open()
        con.execute("UPDATE ruts SET code = ?, desig = ?, forn = ?, order_nr = ?, end_date = ?, last_date = ?, alternative = ?, detail = ?, obs = ?, public = ?, solved = ? WHERE id = ?", (data['code'], data['desig'], data['forn'], data['order'], data['enddate'],data['lastdate'], data['alter'], data['detail'], data['obs'], public, solved , id))
        con.commit()
        con.close()

        # confirm update success and show updated details
        flash('Registo alterado com sucesso')
        return redirect(url_for('details', id=id))

    # if method is GET, render form with data from passed id
    else:
        con = sql_open()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM ruts WHERE id=?", (id,))
        data = cursor.fetchone()
        # pass data to javascript in editform to change select box option according to data in db
        alter = json.dumps(data['alternative'])
        return render_template('editform.html', data=data, alter=alter)

# route to delete data entry, entry to delete id is passed to function
@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    # open db connection and delete entry
    con = sql_open()
    con.execute("DELETE FROM ruts WHERE id = ?", (id,))
    con.commit()
    con.close()
    # confirm successful delete and return to menu
    flash('Registo apagado com sucesso')
    return redirect(url_for('menu'))

if __name__ == "__main__":
    app.run(debug=True)