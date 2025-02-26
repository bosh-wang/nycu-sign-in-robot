from flask import Flask, render_template, request, redirect, url_for, session
import subprocess

import bcrypt

import database

app = Flask(__name__)
app.secret_key = 'signinrobot'

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Preserve the function name for Flask
    return wrap

# In-memory storage for demonstration purposes
submissions = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        email = request.form['email']
        password = request.form['password']
        
        if database.check_login(email, password):
            session['logged_in'] = True
            session['email'] = email
            return render_template('submit.html')
        else:
            return render_template('failed_login.html') 
    
    return render_template('login.html')


@app.route('/dashboard')
# @login_required
def dashboard():
    email = session.get('email')
    # schedule = database.get_schedule_by_email(email)
    # return render_template('dashboard.html', email=email, schedule=schedule)
    return render_template('dashboard.html', email=email)

@app.route('/submit_page', methods=['GET', 'POST'])
def submit_page():
    email = session['email']
    return render_template('submit_page.html', email=email)


@app.route('/submit_schedule', methods=['GET', 'POST'])
@login_required
def submit_schedule():
    if request.method == 'POST':
        
        email = request.form.get('email')
        school_id = request.form.get('school_id')
        password = request.form.get('password')
        schedule = request.form.get('schedule')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
       
        database.insert_schedule(email, password, school_id, schedule, start_time, end_time)


        # open another terminal to run robot stuff
        # subprocess.Popen(['python', 'robot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return redirect(url_for('submit_success'))
    return render_template('submit_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')     
        
        database.register(name, email, hashed_password)

        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/submit_success')
@login_required
def submit_success():
    submission = database.get_one_schedule(session['email'])
    print(submission)
    return render_template('submit_success.html', submission=submission)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
