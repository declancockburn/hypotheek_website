# -*- coding: utf-8 -*-
""" Created by dcockbur (Declan Cockburn) on 4/12/2019 """

# set FLASK_APP=main.py (OR) set FLASK_DEBUG=1
# flask run
# http://localhost:5000/
# https://www.reddit.com/r/learnpython/comments/2ooq1t/im_trying_to_learn_flask_i_want_to_make_a_web_app/

# import secrets
# secrets.token_hex(8)

# Note: shortcuts: ctrl-alt-T, E,
#  fd = {{ $ }},
#  fc = {% $ %},
#  if = {% if $VARIABLE$ %} $END$ {% endif %}

from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import Form, FlaskForm
from wtforms import FloatField
from forms import RegistrationForm, LoginForm, CalcMortgage

app = Flask(__name__)
app.config['SECRET_KEY'] = '3d1405430195b4a9'




posts = [
    {
        "author": "Declan",
        "content": "Test post",
        "date": "12th of april 2019"
    },
    {
        "author": "Dylan",
        "content": "Test post 2",
        "date": "12th of maypril 2019"
    }]

@app.route("/")
def index():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title="ABOOOT")


@app.route("/calculator", methods=['GET', 'POST'])
def calc():

    # class DivideForm(Form):
    #     number = FloatField("Number")
    #     divide_by = FloatField("Divide by")
    #
    # form = DivideForm()
    # result = None
    #
    # if form.validate_on_submit():
    #     result = form.number.data / form.divide_by.data

    m_form = CalcMortgage()
    output = None

    if m_form.validate_on_submit():
        output = m_form.calc()

    return render_template('calculator.html', title="calc", output=output, m_form=m_form)
    # return render_template('calculator.html', title="calc", result=result, form=form, output=output, m_form=m_form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'apexaviour@gmail.com' and form.password.data == '123':
            flash('You\'re logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')

    return render_template('login.html', title='Login', form=form)



    # result = None
    # if request.method == 'POST':
    #     number = float(request.form['number'])
    #     divide_by = float(request.form['divide_by'])
    #     result = number/divide_by
    # return render_template('calculator.html', title="Calculator", result=result)
    #
#
# @app.route("/calc_result", )
# def calc_result():
#
#
#     return render_template('calc_result.html', result=number/divide_by)





if __name__ == '__main__':
    app.run(debug=True)

"""
principal = 200000
int_rate = 0.022
years = 30


payment = principal/(years*12)
tot = 0
for m in range(years*12):
    interest = (principal/12)*int_rate
    print("M: {}, Pr: {}, Rdmptn: {}, Int: {}, tot: {}".format(m+1, principal, payment, interest, interest + payment))
    principal = principal-payment
    tot += payment+interest

print(tot)
"""