# In views/web.py

from flask import Flask, request, render_template, redirect, url_for, session
from core.user_manager import UserManager
from database.mongodb import MongoDB
from utils.email import EmailNotification

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session management

# Initialize the UserManager, MongoDB, and EmailNotification
user_manager = UserManager()
db_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
db_name = "my_weather_app_db"
mongodb = MongoDB(db_uri, db_name)
email_notifier = EmailNotification("smtp.example.com", 587, "your_email@example.com", "your_password")

@app.route('/')
def home():
    return "Welcome to My Weather App"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        watchlist = mongodb.get_watchlist(username)
        return f"Hello, {username}. Your watchlist: {', '.join(watchlist)}"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if 'username' in session:
        username = session['username']
        location = request.form['location']
        mongodb.add_location_to_watchlist(username, location)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
