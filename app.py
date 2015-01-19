from flask import Flask, render_template, request, session,redirect,url_for
import csv
import sqlite3,unicodedata, requests
from utils import manager
from twilio.rest import TwilioRestClient 


app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():

   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() == "profile/":
               print "he"
            else:
               return redirect(manager.getProfilePath())
         if request.form["submit"] == "Make group":
            groupName = request.form["gname"]
            print groupName
            print manager.getTables()
            manager.makeGroup(groupName, username)

      print ids
   else:
      loggedin=False
      username = '-'
   return render_template("base.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/profile/<user>",methods=['GET','POST'])
def profile(user=None):
   ids= manager.getIDs()
   if 'username' in session:
      if request.method=='POST':
         if request.form["submit"] == "Go":
            print manager.getProfilePath()
            if manager.getProfilePath() == "profile/":
               print "he"
            else:
               return redirect(manager.getProfilePath())
         elif request.form["submit"] == "Send":
            print "haha"
            subject = request.form['subject']
            message = request.form['message']
            userexists = False
            first =manager.getFirst(username)        
            last=manager.getLast(username)        
            email=manager.getEmail(username)        
            phone=manager.getPhone(username)        
            facebook=manager.getFacebook(username) 
            email = first + " " + last +"<"+email+">"
            print email
            print number
            manager.sendEmail(email,subject,message)
            manager.sendText2(number,subject,message)
         else:
            print "nada"
      loggedin=True
      username=session['username']
      conn = sqlite3.connect("stem.db")
      c = conn.cursor()

      c.execute("select * from uinfo")

      tabledata = c.fetchall()
      userexists = False
      for d in tabledata:
         if user == d[0]:
            userexists = True
            first = d[2]
            last = d[3]
            phone = d[4]
            email = d[5]
            facebook = d[6]
      
      conn.close()
        
      if userexists == False:
         return render_template("profile.html", userexists=userexists, loggedin=loggedin, username=username,user=user, ids=ids);
      fid=manager.getDefaultPath(user)
      isityou = False
      if user==username:
         isityou=True
      return render_template("profile.html", userexists=userexists, loggedin=loggedin, isityou=isityou, username=username, first=first, last=last, email=email, phone=phone,facebook=facebook, fid=fid, ids=ids)
   else:
      loggedin=False
      username = '-'
      return render_template("profile.html", loggedin=loggedin, username=username,ids=ids)


@app.route("/group/", methods = ['GET', 'POST'])
@app.route("/group/<name>",methods=['GET','POST'])
def group(name=None):
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      if name == None:
         print "hello"
         groupNames=[]
         for n in manager.getTables():
            if n != "uinfo":
               groupNames.append(n)
         return render_template("group.html",loggedin=loggedin, username=username, ids=ids, groupNames=groupNames, name=name) 
      else:
         members= manager.getMemberFacebook(name)
         print members
         return render_template("group.html",loggedin=loggedin,username=username, ids=ids, name=name, members=members)


@app.route("/login",methods=['GET','POST'])
def login():
   ids= manager.getIDs()
   if 'username' in session:
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() == "profile/":
               print "he"
            else:
               return redirect(manager.getProfilePath())
      luser = session['username']
      return render_template("login.html", loggedin=True, username=luser,ids=ids)

   if request.method=='POST':
      
      username = request.form['username']
      password = request.form['password']
      print 'Username and Password have been recorded as variables'
      
      exists = False
      loggedin = False
      reason = ""
      
      conn = sqlite3.connect("stem.db")
      c = conn.cursor()

      c.execute("select * from uinfo")

      tabledata = c.fetchall()
      for d in tabledata:
         if username == d[0]:
            exists = True
            savedpass = d[1]

      conn.close()

      if exists == False:
         reason = "The username "+ username + " does not exist."
            
      if (exists == True and savedpass == password):
         loggedin = True

      if (exists == True and savedpass != password):
         reason = "Your username and password do not match"
 
      if loggedin:
         session['username']=username
      
      return render_template("login.html", loggedin=loggedin, username=username, reason=reason, ids=ids)
   else:
      print session
      return render_template("login.html", loggedin=False, ids=ids)
   #login

@app.route("/logout",methods=['GET','POST'])
def logout():
   ids=manager.getIDs()
   if 'username' in session:
      session.pop('username', None)
      print "login status: logged in"
      return render_template("logout.html", loggedin=False, previous=True, ids=ids)
   else:
      print "login status: not logged in"
      return render_template("logout.html",loggedin=False, previous=False, ids=ids)
   #logout

@app.route("/register",methods=['GET','POST'])
def register():
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() == "profile/":
               print "he"
            else:
               return redirect(manager.getProfilePath())
   else:
      loggedin=False
      username=''

   if request.method=='POST':
      if 'username' not in session:
         username = request.form['username']
         password = request.form['password']
         reppassword = request.form['password2']
         first = request.form['first']
         last = request.form['last']
         email = request.form['email']
         repemail = request.form['email2']
         phone = request.form['phone']

         if 'facebook' in request.form:
            facebook = request.form['facebook']
         else:
            facebook = ""
         
         reason = ""
         registered=False
         
         if password == reppassword:
            registered=True
         else:
            registered=False
            reason = "Passwords do not match"
            print "Passwords do not match"

         if email != repemail:
            registered=False
            reason = "Emails do not match"
            print "Emails do not match"

      conn = sqlite3.connect("stem.db")
      c = conn.cursor()

      c.execute("select * from uinfo")
      tabledata = c.fetchall()
      for d in tabledata:
         if username == d[0]:
            registered=False
            reason="The username "+username+" already exists!"
            print "Username % is already in use" %username

      if registered:
         insinfo="insert into uinfo values ('"+username+"','"+password+"','"+first+"','"+last+"','"+phone+"','"+email+"','"+facebook+"')"
         c.execute(insinfo)
         conn.commit()
         print 'Username and Password have been recorded as variables'
      else:
         print "Failure to register"

      conn.close()

      if registered:
         return render_template("register.html", page=1, username=username,ids=ids)
      return render_template("register.html", page=2, reason=reason,ids=ids)
   else:
      return render_template("register.html", page=3, loggedin=loggedin, username=username, ids=ids) 

@app.route("/edit",methods=['GET','POST'])
def edit():
   ids= manager.getIDs()
   conn = sqlite3.connect("stem.db")
   c = conn.cursor()
  
   if 'username' in session:
      loggedin=True
      username=session['username']
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() == "profile/":
               print "he"
            else:
               return redirect(manager.getProfilePath())
         if request.form["submit"] == "Update":
            first = request.form['first']
            last = request.form['last']
            email = request.form['email']
            phone = request.form['phone']

            if 'facebook' in request.form:
               facebook = request.form['facebook']
            else:
               facebook = ""
            
            insinfo="update uinfo set first='"+first+"',last='"+last+"',phone='"+phone+"',email='"+email+"',facebook='"+facebook+"' where username='"+username+"'"
            c.execute(insinfo)
            conn.commit()
            return render_template("edit.html", updated=True, loggedin=loggedin, username=username, first=first, last=last, email=email, phone=phone,facebook=facebook, ids=ids)

      first =manager.getFirst(username)        
      last=manager.getLast(username)        
      email=manager.getEmail(username)        
      phone=manager.getPhone(username)        
      facebook=manager.getFacebook(username)        
        
      return render_template("edit.html", loggedin=loggedin, username=username, first=first, last=last, email=email, phone=phone,facebook=facebook, ids=ids)
   else:
      loggedin=False
      username = '-'
      return render_template("profile.html", loggedin=loggedin, username=username,ids=ids)


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "STEM"
    app.run()
    
