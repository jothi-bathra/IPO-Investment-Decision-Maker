#Importing required Libraries
#flask for API development
from flask import Flask, request, render_template
#requests and bs4 for web scraping
import requests

import pickle
#numpy for array
import numpy as np

#web scraping for dollar value in INR


#reading .pkl file
path='IPOmodel.pkl'
model = pickle.load(open(path, 'rb'))

#creating instance for Flask 
app=Flask(__name__)
app.secret_key="diam1234"

#getting input from frontend
@app.route('/input',methods=['GET','POST'])
def input():
    details=request.form
    #getting carat, cut, color, clarity, depth and table as input to predict diamond price
    issueSize= float(details['issueSize'])
    issuePrice= int(details['issuePrice'])
    city = int(details['city'])
    country = 0
    industry=float(details['industry'])
    sector=float(details['sector'])
    ecount= float(details['ecount'])
    tshare= int(details['tshare'])
    revenue = int(details['revenue'])
    income = int(details['income'])
    dps=float(details['dividend'])
    liabilities = int(details['liabilities'])
    asset=float(details['asset'])
    rps=revenue/tshare
    ronpe=income/(asset-liabilities)
    dpr=dps/(income/tshare)
    crr=(income-(dps*tshare))/income
        
    print([issueSize ,issuePrice, city, country, industry, sector, ecount,dps,rps,ronpe,dpr,crr])
    #passing values as numpy array and predicting the price in dollar
    prediction = model.predict([[issueSize ,issuePrice, city, country, industry, sector, ecount,dps,rps,ronpe,dpr,crr]])
    #if prediction:
    #    msg='Can be considered for investment'
    #else:
    #    msg='Risk to be invested'
    if prediction[0]==1:
        msg='It will be a profitable investment!!'
    else:
        msg='It is a risky investment!!'
    #rendering price to output page
    return render_template('index.html', msg=msg)
    

#rendering to input page
@app.route('/')
def submit():
    return render_template('index.html')
#main function
if __name__ == '__main__':
    app.run(debug=True)