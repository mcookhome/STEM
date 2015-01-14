from flask import Flask, render_template, request, session,redirect,url_for
import csv
import sqlite3,unicodedata
from utils import manager
app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():

   ids= manager.getIDs()
   if 'username' in session:
      if request.method=='POST':
         if request.form["submit"] == "Go":
            user=request.form["query"]
            path="profile/"+user
            print path
            return redirect(path)
      loggedin=True
      username=session['username']
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
            user=request.form["query"]
            path="profile/"+user
            print path
            return redirect(path)
      loggedin=True
      username=session['username']
      conn = sqlite3.connect("stem.db")
      c = conn.cursor()

      c.execute("select * from uinfo")

      tabledata = c.fetchall()
      for d in tabledata:
         if user == d[0]:
            first = d[2]
            last = d[3]
            email = d[4]
            phone = d[5]
            facebook = d[6]
      fid=""
      rfacebook=facebook[::-1]
      print rfacebook
      for n in rfacebook:
         if (n == "/"):
            break
         else:
            fid = n +fid
            print fid
         
      conn.close()
      return render_template("profile.html", loggedin=loggedin, username=username, first=first, last=last, email=email, phone=phone,facebook=facebook, fid=fid, ids=ids)
   else:
      loggedin=False
      username = '-'
      return render_template("profile.html", loggedin=loggedin, username=username,ids=ids)


@app.route("/login",methods=['GET','POST'])
def login():
   ids= manager.getIDs()
   if 'username' in session:
      if request.method=='POST':
         if request.form["submit"] == "Go":
            user=request.form["query"]
            path="profile/"+user
            print path
            return redirect(path)
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
            user=request.form["query"]
            path="profile/"+user
            print path
            return redirect(path)
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
         doc = [username,password]
         insinfo="insert into uinfo values ('"+username+"','"+password+"','"+first+"','"+last+"','"+email+"','"+phone+"','"+facebook+"')"
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


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "STEM"
    app.run()
    
