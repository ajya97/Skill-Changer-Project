from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/blog"
db = SQLAlchemy(app)

class logindetail(db.Model):
    user_name = db.Column(db.String(50), primary_key=True, nullable=True)
    Name = db.Column(db.String(50), nullable=True)
    Email = db.Column(db.String(50), nullable=True)
    Password = db.Column(db.String(50), nullable=True)
    Ph_num = db.Column(db.Integer(), nullable=True)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['userid']
        password = request.form['pass']
        
        user = logindetail.query.filter_by(user_name=user_name, Password=password).first()

        if user and user.user_name == user_name and user.Password==password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html',name="Wrong User Name and Password")

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register_user():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('Email')
        phone = request.form.get('Phone_num')
        userid = request.form.get('userid')
        password = request.form.get('password')

        entry = logindetail(user_name = userid, Name = name, Email = email, Password= password, Ph_num = phone)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("Register.html")

if __name__ == '__main__':
    app.run(debug=True)

