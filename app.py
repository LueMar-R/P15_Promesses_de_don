from init_bdd import db, collec
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route("/test")
def test():
    collec.insert_one({"firstname": "Lud", "lastname" : "Mai", "amount":100})
    return "Connected to the data base!"

@app.route('/')
def index():
    return redirect(url_for('pourquoi'))

@app.route('/pourquoi')
def pourquoi():
    return render_template('pourquoi.html')

@app.route('/donateurs')
def donateurs():
    date = datetime.datetime.now()
    h = date.hour
    m = date.minute 
    total_recolte =list( collec.aggregate([{ "$group": { "_id" : "null", "somme" : { "$sum": "$total" } } }]) )
    print(total_recolte)
    ont_donne = collec.find({},{"firstname":1, "lastname":1, "total":1})
    return render_template('donateurs.html', heure = h, minute = m, ont_donne=ont_donne, total_recolte=total_recolte[0]['somme'])

@app.route('/donner', methods=('GET', 'POST'))
def donner():
    if request.method == 'POST':
        email = request.values.get('email')
        firstname = request.values.get('firstname')
        lastname = request.values.get('lastname')
        address = request.values.get('address')
        postcode = request.values.get('postcode')
        city = request.values.get('city')
        country = request.values.get('country')
        amount = float(request.values.get('amount'))
        famount = float(request.values.get('famount'))
        total = amount+famount
        hasagreed = request.values.get('hasagreed')
        if not hasagreed: 
            flash('Vous devez accepter les conditions générales !')
        elif not (lastname or firstname) :
            flash('Les champs nom et prénom sont obligatoires !')
        else:
            collec.insert_one({
                "email" : email,
                "firstname" :firstname,
                "lastname" :lastname,
                "address" :address,
                "postcode" :postcode,
                "city" :city,
                "country" :country,
                "total" :total,
                "hasagreed" :hasagreed
                })
            return redirect(url_for('donateurs'))
    return render_template('donner.html')


@app.route('/admin')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        date = datetime.datetime.now()
        h = date.hour
        m = date.minute 
        total_recolte =list( collec.aggregate([{ "$group": { "_id" : "null", "somme" : { "$sum": "$total" } } }]) )
        print(total_recolte)
        ont_donne = collec.find({})
        return render_template('admin.html', heure = h, minute = m, ont_donne=ont_donne, total_recolte=total_recolte[0]['somme'])

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return render_template('admin.html')
    else:
        flash('mot de passe erroné!')
        return render_template('login.html')