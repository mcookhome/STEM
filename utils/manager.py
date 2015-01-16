from flask import Flask, render_template, request, session,redirect,url_for
import csv, unicodedata, requests, sqlite3
from twilio.rest import TwilioRestClient 


def getIDs():
    ids=[]
    conn = sqlite3.connect("stem.db")
    c = conn.cursor()
    c.execute("select * from uinfo")
    tabledata = c.fetchall()
    for d in tabledata:
        ids.append(d[0]);
        conn.close()
    ids[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in ids]
    return ids

def getProfilePath():
    ids=getIDs()
    user=request.form["query"]
    path="profile/"+user
    #if user not in ids:
     #   return ""
    print path
    return path

def sendEmail():
    print "xD"
    return requests.post(
        "https://api.mailgun.net/v2/sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org/messages",
        auth=("api", "key-65c16214d5cecd85f38bfd48f55b2ea3"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org>",
              "to": "poooooooooooN <kevin.poon69@gmail.com>, mchamma <mcookhome@gmail.com>,2sac <terranceliang01@gmail.com>",
              "subject": "POOOOOOOON",
              "text": "POOON DO U SEE THIS IF SO CONTACT ME"}) 


def sendText():
    print "xDtext"
 
    # put your own credentials here 
    ACCOUNT_SID = "AC689ba7d669ce0f609c5645585339ba98" 
    AUTH_TOKEN = "6d116a99af59727ec6f94ac904554933" 
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
    
    client.messages.create(
	to="6466446814", 
	from_="+16468467093", 
	body="poooonn DO U SEE THIS"
    )
