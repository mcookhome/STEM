from flask import Flask, render_template, request, session,redirect,url_for
import csv, unicodedata, requests, sqlite3
from twilio.rest import TwilioRestClient 
import urllib
import urllib2
from datetime import datetime

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

def sendEmail(email,first,last,username,message):
    print "xD"
    e = "2sac <terranceliang01@gmail.com>," + email
    subject = "dllb: Email from "+first + " " + last + " (" + username + ")"
    return requests.post(
        "https://api.mailgun.net/v2/sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org/messages",
        auth=("api", "key-65c16214d5cecd85f38bfd48f55b2ea3"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org>",
              "to": e,
              "subject": subject,
              "text": message}) 


def sendText2(number,first,last,username,message):#uses eztexting bc cheap
    u = "dllbx"
    p = "dllbx"
    m = "dllb: Text from "+first + " " + last + " (" + username + ") " + message
    params = {'User': u,
              'Password': p,
              'PhoneNumbers': number,
              'Message': m}


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
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows



def makeGroup(groupname,maker):
    if groupname in getTables():
        print "table already made"
        return
    if groupname == "":
        print "need a name"
        return
    conn = sqlite3.connect('stem.db')
    cursor = conn.cursor()
    command= "CREATE TABLE '" + groupname+"' (member text, powers text)"
    # Create table
    print command
    cursor.execute(command)
    # Insert a row of data
    addMaker= "INSERT INTO '"+ groupname+ "' VALUES ('"+maker+"', 'admin')"
    print addMaker
    cursor.execute(addMaker)
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS '" + groupname+"' (id integer primary key, user text, message text,  time text)"
    cursor.execute(command)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    initial = "INSERT INTO '"+ groupname+ "'(id,user,message,time) VALUES (1,'"+maker+"','Welcome to "+ groupname+"!','"+time+"')"
    cursor.execute(initial)
    conn.commit()
    conn.close()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS '" + groupname+"' (id integer primary key, user text, name text, description text, duedate text)"
    cursor.execute(command)
    conn.commit()
    conn.close()

def addTask(group,username,name,description,duedate):
    conn=sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    initial = "INSERT INTO '"+ group+ "'(user,name,description,duedate) VALUES ('"+username+"','"+name+"','"+ description+"','"+duedate+"')"
    cursor.execute(initial)
    conn.commit()
    conn.close()


def getItem(table,ovalue,oindex,rindex):
    conn = sqlite3.connect("stem.db")
    c = conn.cursor()
    command = "select * from '" + table +"'"
    c.execute(command)
    tabledata=c.fetchall()
    for d in tabledata:
        if ovalue==d[oindex]:
            value = d[rindex]
    conn.close()
    return value

def getFirst(n):
    first = getItem("uinfo",n,0,2)
    return first
        
def getLast(n):
    last = getItem("uinfo",n,0,3)
    return last
        
def getPhone(n):
    phone = getItem("uinfo",n,0,4)
    return phone

def getEmail(n):
    email = getItem("uinfo",n,0,5)
    return email
        
def getFacebook(n):
    facebook = getItem("uinfo",n,0,6)
    return facebook
        
def getDefaultPath(n):
    fid=""
    rfacebook=getFacebook(n)[::-1]
    for n in rfacebook:
        if (n == "/"):
            break
        else:
            fid = n +fid
    return fid

def getMembers(group):
    conn = sqlite3.connect('stem.db')
    
    with conn:
        
        cursor = conn.cursor()    
        cursor.execute("SELECT member FROM '"+ group+"'")
    
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows

def getMemberFacebook(group):
    members=getMembers(group)
    members[:]=[getDefaultPath(member) for member in members]
    return members

def getPossible(group):
    possible = []
    for n in getIDs():
        if n not in getMembers(group):
            possible.append(n)
    return possible

def addMember(username,name):
    if username not in getIDs():
        print "not a user"
        return
    conn = sqlite3.connect('stem.db')
    cursor = conn.cursor()
    # Insert a row of data
    addMember= "INSERT INTO '"+ name+ "' VALUES ('"+username+"', 'member')"
    print addMember
    cursor.execute(addMember)
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

def getAdmin(name):
    conn = sqlite3.connect("stem.db")
    c = conn.cursor()
    c.execute("select * from '"+name+"'")
    members = c.fetchall()
    for x in members:
        if x[1]=="admin":
            a = x[0]
            conn.close()
            return x[0]
    conn.close()
    return "None"

def removeMember(username,name):
    conn = sqlite3.connect('stem.db')
    cursor = conn.cursor()
    remMember = "DELETE FROM '"+ name + "' WHERE member='"+username+"'"
    print remMember
    cursor.execute(remMember)
    conn.commit()
    conn.close()

def sendMessage(groupname,username, message):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    initial = "INSERT INTO '"+ groupname+ "'(user,message,time) VALUES ('"+username+"','"+message+"','"+time+"')"
    cursor.execute(initial)
    conn.commit()
    conn.close()

def getChat(groupname):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    command = "SELECT * FROM '"+groupname+"'"
    cursor.execute(command)
    chat=cursor.fetchall()
    conn.close()
    return chat

def getTasks(groupname):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    command = "SELECT * FROM '"+groupname+"'"
    cursor.execute(command)
    tasks=cursor.fetchall()
    conn.close()
    return tasks

def removeTask(groupname,taskname):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    remTask = "DELETE FROM '"+ groupname + "' WHERE name='"+taskname+"'"
    print remTask
    cursor.execute(remTask)
    conn.commit()
    conn.close()
