# -*- coding: utf-8 -*-
""" Created by dcockbur (Declan Cockburn) on 4/15/2019 """

from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField#, DateField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import pandas as pd
import numpy as np


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CalcMortgage(Form):
    principal = FloatField("Mortgage Amount")
    int_rate = FloatField("Interest Rate %")
    years = IntegerField("Years")
    submit = SubmitField('Calculate')
    start_date = DateField("Start Date", id='datepick')
    #todo make a date field

    # def __init__(self):
    #     self.df = None
    #     self.total = None

    def calc(self):
        payment = round(self.principal.data / (self.years.data * 12), 2)
        total = 0
        df_data = []
        for m in range(self.years.data * 12):
            interest = round((self.principal.data / 12) * self.int_rate.data, 2)
            df_data.append([m + 1, self.principal.data, payment, interest, interest + payment])
            self.principal.data = round(self.principal.data - payment, 2)
            total += round(payment + interest, 2)
        df = pd.DataFrame(data=df_data, columns=["Month", "Princ", "Redempt. pay", "Int pay", "Tot pay"])
        final = np.sum(df["Tot pay"])
        return f"Total = {final}<br><br>{df.to_html()}"

#
# class Test:
#     principal_mortg = 150000
#     years = 20
#     int_rate = 0.02
#     def calc(self):
#         payment = self.principal_mortg / (self.years * 12)
#         total = 0
#         df_data = []
#         for m in range(self.years * 12):
#             interest = (self.principal_mortg / 12) * self.int_rate
#             df_data.append([m + 1, self.principal_mortg, payment, interest, interest + payment])
#             self.principal_mortg = self.principal_mortg - payment
#             total += payment + interest
#         return pd.DataFrame(data=df_data, columns=["Month", "Princ", "Redempt. pay", "Int pay", "Tot pay"])
#
# test = Test()
#
#
# df = test.calc()
#
# df.to_html()