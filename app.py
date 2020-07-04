#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:06:38 2020

@author: murali
"""
from flask import Flask, request, make_response
import json
import requests
import os
from flask_cors import cross_origin
import pandas as pd
import seaborn as sns
import requests 
from bs4 import BeautifulSoup 
import pymongo
from pymongo import MongoClient
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from report import report
from webscrap import webscrap
from sendemail import sendemail
from pushtodb import pushtodb


app = Flask(__name__)

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()

def webhook():

    req = request.get_json(silent=True, force=True)
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    
    sessionID=req.get('responseId')
    result = req.get("queryResult")
    user_says=result.get("queryText")  
    parameters = result.get("parameters")
    
    intent = result.get("intent").get('displayName')
    
    if (intent=='cust_details'):
        result = req.get("queryResult")
        user_says=result.get("queryText")
        
        parameters = result.get("parameters")
        cust_name=parameters.get("name")
        
        cust_contact = parameters.get("phone")
        cust_email=parameters.get("email")


        #Webscrap from website
        state, state_dic=webscrap.webscrap()
        
        # Pushing data to database
        users_dic=[{"cust_name":cust_name}, {"cust_email":cust_email},{"cust_contact":cust_contact}]
        pushtodb.pushtodb(state_dic, users_dic )
       
        # Report generation
        report.report(state)

        #sending email
        sendemail.sendemail(cust_email)       
        # terminating the session 
        fulfillmentText="Thanks for sharing details, a report has been sent to your email id"
        
        return {
            "fulfillmentText": fulfillmentText
        }
    elif(intent=='stat'):

        state_ut=parameters.get("geo-state")
        
        from pymongo import MongoClient
        from bson.json_util import dumps 
       
        client=MongoClient('mongodb+srv://test:test@cluster0-buydi.mongodb.net/test?retryWrites=true&w=majority')
        mydb=client['covid']
        information=mydb.collection
        statistics=dumps(information.find({"States/UT":state_ut}).limit(1))
        print(statistics)
        string=statistics[47:]
        string=string.replace('"','')
        string=string.replace(']','')
        string=string.replace('}','')

        return {
            "fulfillmentText": string
        }     
    
if __name__ == '__main__':
    app.run(debug=False)
    
