from flask import Flask, render_template, request, session
import csv
import sqlite3

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():
   if 'username' in session:
      loggedin=True
      username=session['username']
   else:
      loggedin=False
      username = '-'
   return render_template("base.html", loggedin=loggedin, username=username)

@app.route("/profile",methods=['GET','POST'])
def profile():
   if 'username' in session:
      loggedin=True
      username=session['username']
            
      conn = sqlite3.connect("stem.db")
      c = conn.cursor()

      c.execute("select * from uinfo")

      tabledata = c.fetchall()
      for d in tabledata:
         if username == d[0]:
            first = d[2]
            last = d[3]
            email = d[4]
            phone = d[5]
            facebook = d[6]

      conn.close()
      return render_template("profile.html", loggedin=loggedin, username=username, first=first, last=last, email=email, phone=phone, facebook=facebook)
   else:
      loggedin=False
      username = '-'
      return render_template("profile.html", loggedin=loggedin, username=username)


@app.route("/login",methods=['GET','POST'])
def login():
   if 'username' in session:
      luser = session['username']
      return render_template("login.html", loggedin=True, username=luser)

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
         reason = "The username "+ username + " does not exists."
            
      if (exists == True and savedpass == password):
         loggedin = True

      if (exists == True and savedpass != password):
         reason = "Your username and password do not match"
 
      if loggedin:
         session['username']=username
      
      return render_template("login.html", loggedin=loggedin, username=username, reason=reason)
   else:
      print session
      return render_template("login.html", loggedin=False)
   #login

@app.route("/logout")
def logout():
   if 'username' in session:
      session.pop('username', None)
      print "login status: logged in"
      return render_template("logout.html", loggedin=False, previous=True)
   else:
      print "login status: not logged in"
      return render_template("logout.html",loggedin=False, previous=False)
   #logout

@app.route("/register",methods=['GET','POST'])
def register():
   if 'username' in session:
      loggedin=True
      username=session['username']
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
            print "Username %s already in use" %username

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
         return render_template("register.html", page=1, username=username)
      return render_template("register.html", page=2, reason=reason)
   else:
      return render_template("register.html", page=3, loggedin=loggedin, username=username) 


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "STEM"
    app.run()
    
