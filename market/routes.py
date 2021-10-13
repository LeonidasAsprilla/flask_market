from market import app
from flask import render_template, redirect, url_for
from flask.helpers import flash
from market.models import Item, User
from market.forms import RegisterForm
from market import db   

@app.route("/pruebas")
def pruebas():
    return render_template('pruebas.html')

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

# @app.route('/about/<username>')
# def about_page(username):
#     return f'<h1>Página Acerca de {username}</h1>'

@app.route('/market')
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                                email_addres=form.email_addres.data,
                                password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Hubo un error con registro de usuario: {err_msg}', category='danger')   

    return render_template('register.html', form=form)