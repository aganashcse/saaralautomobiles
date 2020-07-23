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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Manjapaii$2020@127.0.0.1:3306/saaralhw'
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
INVOICE_NO = ""

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

@app.route('/oldrecord/<part_no>', methods=['GET', 'POST'])
def oldrecord(part_no):
    if Stock.find_by_part_no(part_no):
        part = Stock.find_by_part_no(part_no)[0].json()
        print(part)
        return Response(json.dumps(part), mimetype='application/json')
    return Response(json.dumps([]), mimetype='application/json')

@app.route('/is_record_exists/<part_no>/<price>', methods=['GET', 'POST'])
def is_record_exists(part_no, price):
    if Stock.find_by_part_no_price(part_no, price):
        part = Stock.find_by_part_no_price(part_no, price).json()
        print(part)
        return Response(json.dumps(part), mimetype='application/json')
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
   # stock = Stock(1011, "engine_oil", 500, "2013", 10, 18)
   # stock1 = Stock(1012, "gear_oil", 560, "201", 10, 18)
   # stock2 = Stock(1013, "hydraulic_oil_7.5", 600, "des", 10, 18)
   # stock3 = Stock(1014, "hydraulic_oil_8", 50, 2013, "10", 18)
   # stock.insert_to_db()
   # stock1.insert_to_db()
   # stock2.insert_to_db()
   # stock3.insert_to_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
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
        session['invoice_no'] = request.form.get('invoice_no', "")
        gst = request.form.get("part_gst", "")
        gst_int = int(gst) if gst else 0 
        stock = Stock(session['invoice_no'], request.form['part_no'], request.form.get('part_name', "").lower(), int(request.form['part_price']), request.form.get('part_vehicle_model', "").lower(), request.form.get('part_quantity'), gst_int)
        if Stock.find_by_part_no(request.form['part_no']):
            old_stock = Stock.find_by_part_no(request.form['part_no'])
            old_stock_list = [stock.json() for stock in old_stock]
            print("found old stock:", old_stock_list)
            old_stock_json = json.dumps({"old_stock_list":old_stock_list})
            if old_stock_list[0]['price'] == int(request.form['part_price']):
                stock.quantity = Stock.find_by_part_no_price(request.form['part_no'], request.form['part_price']).quantity + int(request.form['part_quantity'])
                stock.s_no = old_stock_list[0]['s_no']
                print("Stock to be updated:", stock.json())
                stock.update_record()
                return render_template('add_stock.html', invoice_no=session.get('invoice_no', ""), msg="Added Successfully", msg2="", msg_log="Record updated! old: "+old_stock_json, msg1_log="new: "+json.dumps(stock.json())+" in stock db!")
        stock.insert_to_db()
        return render_template('add_stock.html',invoice_no=session.get('invoice_no', ""), msg="Added Successfully", msg_log="New record! "+json.dumps(stock.json())+" added to stock db!")
    return render_template('add_stock.html', invoice_no=session.get('invoice_no', ""))

@app.route('/sale', methods=['GET','POST'])
@flask_login.login_required
def sale():
    return render_template('sale_invoice.html')

@app.route('/jobcard', methods=['GET','POST'])
@flask_login.login_required
def jobcard():
    return render_template('jobcard.html')

@app.route('/add_service_parts', methods=['GET','POST'])
@flask_login.login_required
def add_service_parts():
    return render_template('add_service_parts.html')

@app.route('/delete/<s_no>', methods=['GET','POST'])
@flask_login.login_required
def delete(s_no):
    print("s_no to be deleted:", s_no)
    stock = Stock.find_by_s_no(int(s_no))
    stock.delete_from_db()
    return redirect(url_for('stock'))

@app.route('/stock', methods=['GET'])
@flask_login.login_required
def stock():
    all_stock_objects = Stock.find_all()
    all_stock_dicts = [stock.json() for stock in all_stock_objects]
    total_price = sum([stock['price'] for stock in all_stock_dicts])
    total_quantity = sum([stock['quantity'] for stock in all_stock_dicts])
    total_grand_total = sum([stock['price']+stock['price']*stock['gst']/100 for stock in all_stock_dicts])
    total_s_no = len([stock['s_no'] for stock in all_stock_dicts])
    return render_template('stock.html', all_stock_dicts=all_stock_dicts, total_price=total_price, total_quantity=total_quantity, total_grand_total=total_grand_total, total_s_no=total_s_no)

@app.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=80, debug=True)
