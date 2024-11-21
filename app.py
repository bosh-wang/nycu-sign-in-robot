from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for demonstration purposes
submissions = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        schedule = request.form.get('schedule')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
       
       # Save the data (in-memory for now)
        submissions.append({
            'name': name,
            'email': email,
            'user_id': user_id,
            'password': password,
            'schedule': schedule,
            'start_time': start_time, 
            'end_time' : end_time       
            })

        return redirect(url_for('success'))
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html', submissions=submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
