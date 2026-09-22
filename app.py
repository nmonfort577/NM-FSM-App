from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///students.sqlite3')  # Corrected configuration key and file name
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)  # Corrected class name

def major_enabled():
    env_val = os.environ.get('ENABLE_MAJOR_FIELD')
    if env_val is not None:
        return env_val.strip().lower() in ('true', '1', 'yes', 'on')
    config_val = app.config.get('ENABLE_MAJOR_FIELD')
    if config_val is not None:
        if isinstance(config_val, bool):
            return config_val
        return str(config_val).strip().lower() in ('true', '1', 'yes', 'on')
    return False

class Students(db.Model):  # Corrected class name and capitalization
    id = db.Column('student_id', db.Integer, primary_key=True)  # Corrected column spelling and type
    name = db.Column(db.String(100))  # Corrected column type and spelling
    city = db.Column(db.String(50))  # Corrected column type and spelling
    addr = db.Column(db.String(200))  # Corrected column type and spelling
    pin = db.Column(db.String(10))  # Corrected column type and spelling
    phone = db.Column(db.String(20))
    major = db.Column(db.String(50), nullable=True)

    def __init__(self, name, city, addr, pin, phone=None, major=None):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        self.phone = phone
        self.major = major

@app.route('/')
def show_all():
    return render_template('show_all.html', students=Students.query.all(), show_major=major_enabled())  # Corrected template rendering

@app.route('/new', methods=['GET', 'POST'])
def new():
    show_major = major_enabled()
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            major = request.form.get('major') if show_major else None
            student = Students(
                request.form['name'],
                request.form['city'],
                request.form['addr'],
                request.form['pin'],
                request.form.get('phone', ''),
                major=major
            )
            db.session.add(student)
            db.session.commit()  # Fixed typo in commit
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html', show_major=show_major)

with app.app_context():
    db.create_all()  # Ensure tables are created within the application context
if __name__ == '__main__':
    app.run(debug=True)
