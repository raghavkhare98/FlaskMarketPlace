from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home') #home page so that we can categorize all the webpages. Not really necessary just good practice
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST': #we write this to avoid confirm resubmission on refreshing the page. Post method finalizes the form submission.
        #purchase item logic
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()#object is stored because this object will be used to assign ownership by user id object
        if purchased_item_object: #here ownership is assigned and the budget parameter is decreased
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f'Congratulations! You have successfully purchased {purchased_item_object.name} for ${purchased_item_object.price}', category='success')
            else:
                flash(f'Sorry but you do not have enough credits to purchase {purchased_item_object.name}!', category='danger')

        #sell item logic
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'{sold_item_object.name} sold for ${sold_item_object.price}!')
            else:
                flash(f'Something went wrong with selling {sold_item_object.name}', category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None) #if an item is purchased, it should no longer be displayed hence it is filtered out
        owned_items = Item.query.filter_by(owner=current_user.id)#to show the items owned by the current user
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET','POST']) #using methods to handle post requests.Posts requests are necessary for the submission of forms
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created succesfully. You are now logged in as, {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: # the form object stores it's errors in a dictionary, hence if the dictionary is empty, then the form was submitted succesfully
        for err_msg in form.errors.values():
            flash(f'There was an error in generating the user:{err_msg}', category='danger') #this works the same way as print but will display the message on the website instead of server side
    return render_template('register.html', form=form)      #we wrote category as danger because importing the boostrap calss which
                                                            #will display a red colored error message is named danger and this code will be
                                                            #read in the base html file


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user) #the login user function will log in the user. This function returns true if successful false if not
            flash(f'Succesfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password do not match. Please check your login credentials and try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logut', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash('You have been succesfully logged out!', category='info')
    return redirect(url_for("home_page"))
