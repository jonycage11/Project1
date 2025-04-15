from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory user storage (for demo purposes)
users = {}
tasks = {}

@app.route('/')
def index():
    if 'user' in session:
        user_tasks = tasks.get(session['user'], [])
        return render_template('index.html', user=session['user'], tasks=user_tasks)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users:
            hashed_password = generate_password_hash(password)
            users[username] = {'password': hashed_password}
            return redirect(url_for('login'))
        return "Username already taken"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user' in session:
        task = request.form['task']
        if task:
            user_tasks = tasks.get(session['user'], [])
            user_tasks.append(task)
            tasks[session['user']] = user_tasks
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/delete_task/<task>')
def delete_task(task):
    if 'user' in session:
        user_tasks = tasks.get(session['user'], [])
        if task in user_tasks:
            user_tasks.remove(task)
            tasks[session['user']] = user_tasks
        return redirect(url_for('index'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
