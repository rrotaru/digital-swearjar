# -*- coding: utf-8 -*-
from __future__ import division
from datetime import timedelta
from flask import Flask, Response
from flask import make_response, request, current_app
from flask import render_template, redirect, jsonify, send_from_directory
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
    content = get_file('index.html')
    return Response(content, mimetype="text/html")

#API Call to show balance
@app.route("/balance",methods=['POST'])
def show_balance():
    payload = {'password':request.form['password']}
    guid = request.form['guid']

    baseurl = "https://blockchain.info/merchant/"+request.form['guid']+"/balance"
    r = requests.post(baseurl,data=payload)
    jsondata = r.json()
    return jsonify(**jsondata)

    #balance = str((jsondata['balance']) / 100000000)
    #return balance

#API call to send payments to other accounts
@app.route("/payment", methods=['POST'])
def make_payment():
    payload = {
            'password':request.form['password'], 
            'to':request.form['to'], 
            'note':request.form.get('note', "")    
    }
    guid = request.form['guid']    

    baseurl = "https://blockchain.info/merchant/"+guid+"/payment"
    r = requests.post(baseurl,data=payload)
    jsondata = r.json()
    return jsonify(**jsondata)

@app.route("/create_wallet", methods=['POST'])
def create_wallet():
    print request, request.form, request.form['password']
    payload = {
            'api_code': request.form['api_code'],
            'password': request.form['password'],
            'email': request.form.get('email', ""),
            'label': request.form.get('label', ""),
    }

    baseurl = "https://blockchain.info/api/v2/create_wallet"
    r = requests.post(baseurl,data=payload)
    try:
        jsondata = r.json()
        return jsonify(**jsondata)
    except Exception as e:
        print "Error: ", e
        return r.text

@app.route("/new_address", methods=['POST'])
def new_address():
    payload = {
            'password': request.form['password'],
            'label': request.form.get('label', "")
    }
    guid = request.form['guid']

    baseurl = "https://blockchain.info/merchant/"+guid+"/new_address"

    r = requests.post(baseurl,data=payload)
    jsondata = r.json()
    return jsonify(**jsondata)

@app.route("/list", methods=['POST'])
def list():
    print "here"
    payload = {
            'password': request.form['password']
    }
    print "here2"
    guid = request.form['guid']
    
    print "here3"
    baseurl = "https://blockchain.info/merchant/"+guid+"/list"
    print "here4" 
    r = requests.post(baseurl,data=payload)
    print r.text
    jsondata = r.json()
    return jsonify(**jsondata)

@app.route('/js/<path:path>')
def send_js(path):
    content = get_file('js/'+path);
    return Response(content, mimetype="text/javascript")

@app.route('/css/<path:path>')
def send_css(path):
    content = get_file('css/'+path);
    return Response(content, mimetype="text/css")

