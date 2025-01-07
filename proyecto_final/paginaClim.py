from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '36222963'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado')
            return redirect(url_for('register'))
        
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso! Por favor inicia sesión')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Has iniciado sesión correctamente!')
            return redirect(url_for('index'))
        
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        email = request.form.get('email')
        content = request.form.get('text')
        
        if not email or not content:
            flash('Por favor completa todos los campos')
            return redirect(url_for('index', _anchor='feedback'))
        
        # Crear nuevo comentario
        new_comment = Comment(email=email, content=content)
        db.session.add(new_comment)
        
        try:
            db.session.commit()
            flash('¡Tu mensaje ha sido enviado exitosamente!')
        except:
            db.session.rollback()
            flash('Hubo un error al enviar tu mensaje. Por favor intenta de nuevo.')
        
        return redirect(url_for('index', _anchor='feedback'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)