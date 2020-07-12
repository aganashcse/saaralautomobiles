import flask_login
import json

from flask import Flask, request, url_for, render_template, session, redirect, Response
from flask_mail import Mail, Message
from models.stock import Stock

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flask.ganesh@gmail.com'
app.config['MAIL_PASSWORD'] = 'slmvveqoktmewnyf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/saaralhw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'ganesha'
mail = Mail(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#CONSTANTS
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"
USER = "user"
PASSWORD = "user"

#flask_login section
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = session['user_id']
    return user

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    if Stock.find_all():
        parts = [stock.part_name for stock in Stock.find_all()]
        print(parts)
        return Response(json.dumps(parts), mimetype='application/json')
    return Response(json.dumps([]), mimetype='application/json')

@app.route('/_oldrecord/<part_no>', methods=['GET'])
def oldrecord(part_no):
    if Stock.find_by_part_no(request.form['part_no']):
        part = list(Stock.find_by_part_no(request.form['part_no']).json())
        print(parts)
        return Response(json.dumps(parts), mimetype='application/json')
    return Response(json.dumps([]), mimetype='application/json')

@app.route('/_autopart_no', methods=['GET'])
def autopart_no():
    if Stock.find_all():
        parts = [str(stock.part_no) for stock in Stock.find_all()]
        print(parts)
        return Response(json.dumps(parts), mimetype='application/json')
    return Response(json.dumps([]), mimetype='application/json')

@app.route('/_autovehicle_model', methods=['GET'])
def autovehicle_model():
    if Stock.find_all():
        parts = [str(stock.vehicle_model) for stock in Stock.find_all()]
        print(parts)
        return Response(json.dumps(parts), mimetype='application/json')
    return Response(json.dumps([]), mimetype='application/json')

@app.before_first_request
def create_tables():
    db.create_all()
    # stock = Stock(1011, "Engine_oil", 500, "2013", 10, 18)
    # stock1 = Stock(1012, "Gear_oil", 560, "201", 10, 18)
    # stock2 = Stock(1013, "Hydraulic_oil_7.5", 600, "des", 10, 18)
    # stock3 = Stock(1014, "Hydraulic_oil_8", 50, 2013, "10", 18)
    # stock.insert_to_db()
    # stock1.insert_to_db()
    # stock2.insert_to_db()
    # stock3.insert_to_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    session['user_id']=request.form['user_id'].lower()
    if session['user_id'] == ADMIN_USER:
        if request.form['user_passwd'].lower() == ADMIN_PASSWORD:
            user_obj = User()
            user_obj.id = session['user_id']
            flask_login.login_user(user_obj)
            return redirect(url_for('homepage'))
        return render_template('index.html', msg = 'Password is incorrect!')
    else:
        if session['user_id'] == USER:
            if request.form['user_passwd'].lower() == PASSWORD:
                user = User()
                user.id = session['user_id']
                flask_login.login_user(user)
                return redirect(url_for('homepage'))
            return render_template('index.html', msg = 'Password is incorrect!')
        return render_template('index.html', msg = 'User ID is incorrect!')

@app.route('/homepage', methods=['GET','POST'])
@flask_login.login_required
def homepage():
    return render_template('homepage.html')

@app.route('/add_stock', methods=['GET','POST'])
@flask_login.login_required
def add_stock():
    if request.method=='POST':
        stock = Stock(request.form['part_no'], request.form['part_name'].lower(), request.form['part_price'], request.form['part_vehicle_model'].lower(), request.form['part_quantity'], request.form['part_gst'])
        if Stock.find_by_part_no(request.form['part_no']):
            old_stock = Stock.find_by_part_no(request.form['part_no'])
            print("found old stock:", old_stock.json())
            stock.quantity = old_stock.quantity + int(request.form['part_quantity'])
            print("Stock to be updated:", stock.json())
            stock.update_record()
            return render_template('add_stock.html', msg="Record updated! old: "+json.dumps(old_stock.json()), msg1="new: "+json.dumps(stock.json())+" in stock db!")
        stock.insert_to_db()
        return render_template('add_stock.html', msg="New record! "+json.dumps(stock.json())+" added to stock db!")
    return render_template('add_stock.html')

@app.route('/sale', methods=['GET','POST'])
@flask_login.login_required
def sale():
    return render_template('sale.html')

@app.route('/jobcard', methods=['GET','POST'])
@flask_login.login_required
def jobcard():
    return render_template('jobcard.html')

@app.route('/add_service_parts', methods=['GET','POST'])
@flask_login.login_required
def add_service_parts():
    return render_template('add_service_parts.html')

@app.route('/stock', methods=['GET'])
@flask_login.login_required
def stock():
    all_stock_objects = Stock.find_all()
    all_stock_dicts = [stock.json() for stock in all_stock_objects]
    return render_template('stock.html', all_stock_dicts=all_stock_dicts)

@app.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=2222, debug=True)