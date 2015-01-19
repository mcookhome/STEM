from flask import Flask, render_template, request, session,redirect,url_for
import csv, unicodedata, requests, sqlite3
from twilio.rest import TwilioRestClient 
import urllib
import urllib2

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

def sendEmail(email,subject,message):
    print "xD"
    e = "2sac <terranceliang01@gmail.com>," + email
    return requests.post(
        "https://api.mailgun.net/v2/sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org/messages",
        auth=("api", "key-65c16214d5cecd85f38bfd48f55b2ea3"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org>",
              "to": e,
              "subject": subject,
              "text": message}) 


def sendText2(number,subject,message):#uses eztexting bc cheap
    u = "xdllb"
    p = "xdllb"

    params = {'User': u,
              'Password': p,
              'PhoneNumbers': number,
              'Subject': subject,
              'Message': message}


    url = "https://app.eztexting.com/sending/messages?format=json"
    
    u = urllib.urlopen(url,urllib.urlencode(params))
    print "ayylmao"
    print u.read()
    
def sendTextTwilio():#too much money :(
    print "xDtext"
 
    # put your own credentials here 
    ACCOUNT_SID = "AC689ba7d669ce0f609c5645585339ba98" 
    AUTH_TOKEN = "6d116a99af59727ec6f94ac904554933" 
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
    
    client.messages.create(
	to="4048387321", 
	from_="+16468467093", 
	body="poooonn DO U SEE THIS"
    )

def getTables():
    conn = sqlite3.connect('stem.db')

    with conn:
    
        cursor = conn.cursor()    
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
        rows = cursor.fetchall()
        print rows
        for row in rows:
            print "help"
            print row[0]

def makeGroup(groupname,maker):
    conn = sqlite3.connect('stem.db')
    cursor = conn.cursor()
    command= "CREATE TABLE " + groupname+" (member text, powers text)"
    # Create table
    print command
    cursor.execute(command)
    # Insert a row of data
    addMaker= "INSERT INTO "+ groupname+ " VALUES ('"+maker+"', 'admin')"
    print addMaker
    cursor.execute(addMaker)
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
