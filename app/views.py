from __future__ import division
from flask import render_template, redirect
from app import app
import requests
import json

#The base html page, nothing here yet
@app.route("/")
def hello():
    return "Hello World!"

#API Call to show balance
@app.route("/account_balance/<path:account_number>/<path:password>")
def show_balance(account_number, password):
    guid = account_number 
    main_password = password

    baseurl = "https://blockchain.info/merchant/"+guid+"/balance?password="+main_password
    
    r = requests.get(baseurl)
    jsondata = r.json()

    balance = str((jsondata['balance']) / 100000000)

    return balance

#API call to send payments to other accounts
@app.route("/payment/<path:account_number>/<path:password>/<path:address>/<path:amount>/")
def make_payment(account_number, password, address, amount):
    account_number = account_number
    password = password
    address = address
    amount = amount

    baseurl = "https://blockchain.info/merchant/"+account_number+"/payment?password="+password+"&to="+address+"&amount="+amount

    r = requests.get(baseurl)
    jsondata = r.json()

    message = str(jsondata['message'])

    return message 
