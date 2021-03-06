from os import name
from market import app
from flask import render_template, redirect, url_for, request
from flask.helpers import flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db   
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method=="POST":
        # Lógica de Items Comprados
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Felicitaciones! Has comprado {p_item_object.name} por ${p_item_object.price}", category="success")
            else:
                flash(f"Desafortunadamente, no tienes dinero suficiente para comprar {p_item_object.name}", category="danger")
        # Lógica de Items Vendidos
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Felicitaciones! Has vendido {s_item_object.name} de regreso al Market!", category="success")
            else:
                flash(f"Algo salio mal con la venta de {s_item_object.name}", category="danger")

        return redirect(url_for('market_page'))
    
    if request.method=="GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                                email_addres=form.email_addres.data,
                                # password_hash=form.password1.data)
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Cuenta creada con exito! Ahora has ingresado como {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Hubo un error con registro de usuario: {err_msg}', category='danger')   

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Exito! Has ingresado como: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Nombre de Usuario y Contraseña Incorrectos! Por favor intente nuevamente.', category='danger')
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Te has desconectado con exito!", category='info')
    return redirect(url_for("home_page"))