from flask import request, session, redirect, url_for, render_template, flash

from . models import Models
from . forms import SignUpForm, SignInForm

from src import app

models = Models()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pos')
def show_pos():
    try:
        if session['user_available']:
            pos = models.getAllPos()
            return render_template('pos.html', pos=pos)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/product')
def show_product():
    try:
        if session['user_available']:
            product = models.getAllProduct()
            return render_template('product.html', product=product)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/date')
def show_date():
    try:
        if session['user_available']:
            date = models.getAllDate()
            return render_template('date.html', date=date)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/store')
def show_store():
    try:
        if session['user_available']:
            store = models.getAllStore()
            return render_template('store.html', store=store)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/statisticsday')
def show_statisticsday():
    try:
        if session['user_available']:
            day = models.getDayStatistics()
            return render_template('statistics_day.html',day=day)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/statistics')
def show_statistics():
    try:
        if session['user_available']:
            return render_template('statistics.html')
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/store_sales')
def show_store_sales():
    try:
        if session['user_available']:
            storetotalsales = models.getStoreTotalSales()
            return render_template('statistics_store_sales.html', storetotalsales=storetotalsales)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        
@app.route('/statisticsmonth')
def show_statisticsmonth():
    try:
        if session['user_available']:
            month = models.getMonthStatistics()
            return render_template('statistics_month.html',month=month)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
    
@app.route('/product_sales')
def show_product_sales():
    try:
        if session['user_available']:
            product = models.getProductSales()
            return render_template('statistics_product_sales.html',product=product)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/store_month')
def show_store_month():
    try:
        if session['user_available']:
            store_month = models.getStoreMonth()
            return render_template('statistics_store_month.html',store_month=store_month)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/store_day')
def show_store_day():
    try:
        if session['user_available']:
            store_day = models.getStoreDay()
            return render_template('statistics_store_day.html',store_day=store_day)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/product_day')
def show_product_day():
    try:
        if session['user_available']:
            product_day = models.getProductDay()
            return render_template('statistics_product_day.html',product_day=product_day)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/product_month')
def show_product_month():
    try:
        if session['user_available']:
            product_month = models.getProductMonth()
            return render_template('statistics_product_month.html',product_month=product_month)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        # Create a new user and add them to the SQL table
        new_user = User(email=email, password=password)  # Create a User object
        db.session.add(new_user)  # Add the user to the session
        db.session.commit()  # Commit the session to save the user to the database

        flash('User registered successfully', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        signinform = SignInForm(request.form)
        if request.method == 'POST':
            em = signinform.email.data
            log = models.getUserByEmail(em)
            if log.password == signinform.password.data:
                session['current_user'] = em
                session['user_available'] = True
                return redirect(url_for('show_pos'))
            else:
                flash('Cannot sign in')
        return render_template('signin.html', signinform=signinform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/about_user')
def about_user():
    try:
        if session['user_available']:
            user = models.getUserByEmail(session['current_user'])
            return render_template('about_user.html', user=user)
        flash('You are not an Authenticated User')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    try:
        session.clear()
        session['user_available'] = False
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
