from flask import Flask, render_template, request, redirect, url_for
import subprocess

import bcrypt

import database

app = Flask(__name__)

# In-memory storage for demonstration purposes
submissions = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        email = request.form['email']
        # password = request.form['password'].encode('utf-8')
        password = request.form['password']
        
        if database.check_login(email, password):
            return render_template('submit.html')
        else:
            return render_template('failed_login.html') 
    
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        school_id = request.form.get('school_id')
        password = request.form.get('password')
        schedule = request.form.get('schedule')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
       
       
        submissions.append({
            'name': name,
            'email': email,
            'school_id': school_id,
            'password': password,
            'schedule': schedule,
            'start_time': start_time, 
            'end_time' : end_time       
            })
        
        database.insert_user(name, password, email, school_id)
        database.insert_schedule(school_id, schedule, start_time, end_time)


        # open another terminal to run robot stuff
        subprocess.Popen(['python', 'robot.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return redirect(url_for('success'))
    return render_template('submit.html')

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


@app.route('/success')
def success():
    return render_template('success.html', submissions=submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
