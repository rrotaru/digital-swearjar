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

@app.route("/create_wallet/<path:password>/<path:label>/<path:email>")
def create_wallet(password, label, email):
    password = password
    label = label
    email = email

    baseurl = "https://blockchain.info/api/v2/create_wallet?password="+password+"&label="+label+"&api_code=6c58b8d9-f429-4af0-a7ae-be98dbeb62f8&"+email

    r = requests.get(baseurl)
    try:
        jsondata = r.json()
    except Exception as e:
        print e

    guid = jsondata['guid']
    link = jsondata['link']

    return ("New GUID: %s @ %s" % (guid, link))

@app.route("/new_address/<path:guid>/<path:password>/<path:label>")
def new_address(guid, password, label):
    guid = guid
    password = password
    label = label

    baseurl = "https://blockchain.info/merchant/"+guid+"/new_address?password="+password+"&label="+label
    """
    r = requests.get(baseurl)
    jsondata = r.json()

    address = jsondata['address']
    label = jsondata['label']
    """

    return ("Created new address: %s named: %s" % (address, label))
