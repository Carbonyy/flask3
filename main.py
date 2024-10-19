from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mega_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        login_email = request.form['login_email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        speciality = request.form['speciality']
        address = request.form['address']

        if password != repeat_password:
            flash('Пароли не совпадают!')
            return redirect(url_for('home'))

        hashed_password = generate_password_hash(password=password, method='pbkdf2:sha1', salt_length=8)

        new_user = User(login_email=login_email, password=hashed_password, surname=surname, name=name, age=age, speciality=speciality, address=address)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!')
        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
