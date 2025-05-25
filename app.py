from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/blog"
app.secret_key = 'secret'
db = SQLAlchemy(app)

class logindetail(db.Model):
    user_name = db.Column(db.String(50), primary_key=True, nullable=True)
    Name = db.Column(db.String(50), nullable=True)
    Email = db.Column(db.String(50), nullable=True)
    Password = db.Column(db.String(50), nullable=True)
    Ph_num = db.Column(db.Integer(), nullable=True)
    Location = db.Column(db.String(50), nullable=False)
    Skills_Offered = db.Column(db.String(50), nullable=False)
    Skills_Wanted = db.Column(db.String(50), nullable=False)
    Availability = db.Column(db.String(50), nullable=False)
    Bio = db.Column(db.String(500), nullable=False)



# index.html page
@app.route('/')
def index():
    o = logindetail()
    print(o.Name)
    return render_template('index.html')

# home page
@app.route('/home', methods=['GET','POST'])
def home():
    username = session.get('user', 'Guest')
    pas = session.get('pas', 'No pas')
    user = logindetail.query.filter_by(user_name=username, Password=pas).first()
    if user:
        return render_template('home.html',name=user.Name)
    else:
        return render_template('index.html')

# profile page
@app.route('/profile', methods=['GET','POST'])
def profile():
    username = session.get('user', 'Guest')
    pas = session.get('pas', 'No pas')
    user = logindetail.query.filter_by(user_name=username, Password=pas).first()
    if user:
        return render_template('profile.html',name=user.Name, email= user.Email, loc= user.Location, so= user.Skills_Offered, sw= user.Skills_Wanted, ava= user.Availability, phone= user.Ph_num, bio= user.Bio)
    else:
        return render_template('index.html')
    

# edit profile
@app.route('/editprofile', methods=['GET','POST'])
def editprofile():
    username = session.get('user', 'Guest')
    pas = session.get('pas', 'No pas')
    user = logindetail.query.filter_by(user_name=username, Password=pas).first()
    if(request.method=='POST'):
        user.Name = request.form.get('fullname')
        user.Location = request.form.get('location')
        user.Skills_Offered = request.form.get('skills_offered')
        user.Skills_Wanted = request.form.get('skills_wanted')
        user.Availability = request.form.get('availability')
        user.Ph_num = request.form.get('contact')
        user.Bio = request.form.get('bio')
        db.session.commit()

        return redirect(url_for('profile'))
    if user:
        return render_template('editprofile.html',name=user.Name)
    # return render_template("editprofile.html")


@app.route('/login', methods=['GET','POST'])
def login():
    session['user'] = ""
    session['pas'] = ""
    if request.method == 'POST':
        user_name = request.form['userid']
        password = request.form['pass']
        
        user = logindetail.query.filter_by(user_name=user_name, Password=password).first()

        if user and user.user_name == user_name and user.Password==password:
            session['user'] = user_name
            session['pas'] = password
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
        session['user'] = userid
        session['pas'] = password
        return redirect(url_for('home'))
    return render_template("Register.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

