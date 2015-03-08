# -*- coding: utf-8 -*-
from __future__ import division
from datetime import timedelta
from flask import Flask, Response
from flask import make_response, request, current_app
from flask import render_template, redirect, jsonify
from functools import update_wrapper
from app import app
import requests
import json
import os.path

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

#The base html page, nothing here yet
@app.route("/")
def hello():
    content = get_file('../index.html')
    return Response(content, mimetype="text/html")

#API Call to show balance
@app.route("/balance",methods=['POST'])
def show_balance():
    payload = {'password':request.form['password']}
    guid = request.form['guid']
    print payload, guid

    baseurl = "https://blockchain.info/merchant/"+request.form['guid']+"/balance"
    r = requests.post(baseurl,data=payload)
    jsondata = r.json()
    print jsondata
    return jsonify(**jsondata)

    #balance = str((jsondata['balance']) / 100000000)
    #return balance

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
