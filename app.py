from flask import Flask, render_template, request, redirect, url_for
import subprocess

import database

app = Flask(__name__)

# In-memory storage for demonstration purposes
submissions = []

@app.route('/', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html', submissions=submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
