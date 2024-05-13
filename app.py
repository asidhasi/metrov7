from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'abcdefghijk'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Cust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)



@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
    #     if user:
    #         return redirect(url_for('customer'))
    #     elif request.form['username'] != "username" and request.form['password'] != 'password':
    #         error = "Wrong Username or Password"
    #         return render_template("ex.html", error=error)
    #     else:
    #         return redirect(url_for('signup'))
    # return render_template('ex.html')

        if not user:
            return redirect(url_for('signup'))
        elif request.form['username'] != "username" and request.form['password'] != 'password':
            error = "Wrong Username or Password"
            return render_template("ex.html", error=error)
        else:
            return redirect(url_for('customer'))
    return render_template('ex.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    msg1 = None
    msg2 = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            msg1 = "User already exist"
            return render_template('signup.html',msg1=msg1)
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    msg2 = "If you don't have any account , please signup"
    return render_template('signup.html',msg2=msg2)


@app.route('/customer', methods=["GET", "POST"])
def customer():
     if request.method == 'POST':
         name = request.form['name']
         address = request.form['address']
         email = request.form['email']
         phone = request.form['phone']


         new_cust = Cust(name=name, address=address, email=email, phone=phone)
         db.session.add(new_cust)
         # db.session.commit()
         results = request.form
         return render_template("details.html",formdata=results)

     return render_template("customer.html")


@app.route('/details', methods =['POST', 'GET'])
def details():
    if request.method == 'POST':
        results = request.form
        return render_template('details.html', formdata=results)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
