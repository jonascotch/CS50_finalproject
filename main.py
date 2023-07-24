from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = "Your_secret_string"

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/login', methods=("POST", "GET"))
def login():
    if request.method == "POST":
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/menu', methods=("POST", "GET"))
def menu():
    if request.method == "POST":
        return render_template('menu.html')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)