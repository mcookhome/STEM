from flask import Flask, render_template, request, session,redirect,url_for
import csv
import sqlite3,unicodedata, requests
from utils import manager
from twilio.rest import TwilioRestClient 
from datetime import datetime

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():
   
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() != "profile/":
               return redirect(manager.getProfilePath())
         if request.form["submit"] == "Make group":
            groupName = request.form["gname"]
            print groupName
            print manager.getTables()
            manager.makeGroup(groupName, username)
            return redirect("group/"+groupName)

      print ids
      return render_template("base.html", loggedin=loggedin, username=username,ids=ids,myGroups=myGroups,notifs=notifs)
   else:
      loggedin=False
      username = '-'
      return render_template("base.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/profile/<user>",methods=['GET','POST'])
def profile(user=None):
   ids= manager.getIDs()
   if 'username' in session:
      username=session['username']
      userGroups = manager.getUserGroups(user);
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      print userGroups;

      if request.method=='POST':
         if request.form["submit"] == "Go":
            print manager.getProfilePath()
            if manager.getProfilePath() != "profile/":
               return redirect(manager.getProfilePath())
         elif request.form["submit"] == "Dual Contact":
            print "haha"
            message = request.form['message']
            userexists = False
            first =manager.getFirst(username)        
            last=manager.getLast(username)        
            email=manager.getEmail(user)        
            phone=manager.getPhone(user)
            sfirst=manager.getFirst(user)
            slast=manager.getLast(user)
            email = sfirst + " " + slast +"<"+email+">"
            print email
            print phone
            manager.sendEmail(email,first,last,username,message)
            print"success with email"
            try:
               manager.sendText2(phone,first,last,username,message)
               print "success with text"
            except Exceptions:
               pass
         else:
            print "nada"
      loggedin=True
      conn = sqlite3.connect("databases/users.db")
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
         return render_template("profile.html", userexists=userexists, loggedin=loggedin, username=username,user=user, ids=ids, userGroups=userGroups,myGroups=myGroups,notifs=notifs);
      fid=manager.getDefaultPath(user)
      isityou = False
      if user==username:
         isityou=True
      return render_template("profile.html", userexists=userexists, loggedin=loggedin, isityou=isityou, username=username, first=first, last=last, email=email, phone=phone,facebook=facebook, fid=fid, ids=ids, userGroups=userGroups,myGroups=myGroups,notifs=notifs)
   else:
	  loggedin=False
	  username = '-'
	  return render_template("profile.html", loggedin=loggedin, username=username,ids=ids, userGroups=userGroups)


@app.route("/create",methods=['GET', 'POST'])
def createGroup():
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() != "profile/":
               return redirect(manager.getProfilePath())
         if request.form["submit"] == "Make group":
            groupName = request.form["gname"]
            print groupName
            print manager.getTables()
            manager.makeGroup(groupName, username)
            return redirect("group/"+groupName)

      print ids
   else:
      loggedin=False
      username = '-'
   return render_template("create.html", loggedin=loggedin, username=username,ids=ids,myGroups=myGroups,notifs=notifs)

@app.route("/about/", methods = ['GET','POST'])
def about():
   ids= manager.getIDs()
   loggedin = False
   username='-'
   myGroups='-'
   notifs='-'
   if 'username' in session:
      loggedin=True
      username=session['username']
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      if request.method=='POST':
         if "submit" in request.form:
            if request.form["submit"] == "Go":
               print manager.getProfilePath()
               if manager.getProfilePath() != "profile/":
                  return redirect(manager.getProfilePath())
   return render_template("about.html",loggedin=loggedin, username=username, ids=ids, myGroups=myGroups, notifs=notifs)

@app.route("/group/", methods = ['GET', 'POST'])
@app.route("/group/<name>",methods=['GET','POST'])
def group(name=None):
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      if request.method=='POST':
         if "submit" in request.form:
            if request.form["submit"] == "Go":
               print manager.getProfilePath()
               if manager.getProfilePath() != "profile/":
                  return redirect(manager.getProfilePath())
            if request.form["submit"] == "Request To Join":
               manager.joinReq(name, username)
      if name == None:
         print "hello"
         groupNames=[]
         for n in manager.getTables():
            groupNames.append(n)
         return render_template("group.html",loggedin=loggedin, username=username, ids=ids, groupNames=groupNames, name=name,myGroups=myGroups,notifs=notifs)
      elif name not in manager.getTables():
         return redirect("/group/")
      else:
         requested=manager.hasRequested(name, username)
         reqMems=manager.requeMems(name,username)
         admin = manager.getAdmin(name)
         tasks=sorted(manager.getTasks(name), key=lambda t: t[4])
         if request.method=='POST':
            print "POST"
            members=manager.getMembers(name)
            if "submit" in request.form:
               if request.form["submit"] == "Add member":
                  print "ldlddlld"
                  requestedMember=request.form["member"]
                  manager.addMember(requestedMember,name)
               if request.form["submit"] == "Leave":
                  if username == admin:
                     manager.disbandGroup(name)
                     return redirect("/group")
                  else:
                     manager.removeMember(username,name)
               if request.form["submit"]== "Dual Contact":
                  message=request.form["message"]
                  members=manager.getMembers(name)
                  for user in members:
                     if user != username:
                        first =manager.getFirst(username)        
                        last=manager.getLast(username)        
                        email=manager.getEmail(user)        
                        phone=manager.getPhone(user)
                        sfirst=manager.getFirst(user)
                        slast=manager.getLast(user)
                        email = sfirst + " " + slast +"<"+email+">"
                        print email
                        print phone
                        manager.sendEmail(email,first,last,username,message)
                        print"success with email"
                        try:
                           manager.sendText2(phone,first,last,username,message)
                           print "success with text"
                        except Exceptions:
                           pass
            elif "sendmessage" in request.form:
               mess = request.form["message"]
               manager.sendMessage(name,username,mess)
            elif "addtask" in request.form:
               taskname=request.form["taskname"]
               desc=request.form["description"]
               ddate=request.form["year"]+"-"+request.form["month"]+"-"+request.form["date"]
               manager.addTask(name,username,taskname,desc,ddate)
               return redirect("/group/"+name)
            else:
               for x in request.form:
                  print x
                  if request.form[x]=="Approve":
                     print "approved"
                     manager.addMember(x,name)
                     manager.ridRequest(name,x)
                  if request.form[x]=="Deny":
                     
                     manager.denyRequest(name,x)
                  for task in tasks:
                     if task[2]==x:
                        print "removing task"
                        manager.removeTask(name,x,username)
                        return redirect("/group/"+name)
               print "BLAH"
               for rmem in members:
                  print "HAH"
                  if rmem in request.form:
                     print "REMOVING"
                     manager.removeMember(rmem,name)
         members=manager.getMembers(name)
         fmembers= manager.getMemberFacebook(name)
         print members
         possible=manager.getPossible(name)
         print ids
         reqMems=manager.requeMems(name,username)
         print possible
         chat = manager.getChat(name)
         hasTasks = len(tasks) > 0;
         lenmembers = len(fmembers);
         return render_template("group.html",loggedin=loggedin, admin=admin, username=username, ids=ids, name=name, members=members, lenmembers=lenmembers, fmembers=fmembers, possible=possible,chatlog=chat,tasklist=tasks,myGroups=myGroups,notifs=notifs,requested=requested,reqMems=reqMems, hasTasks=hasTasks)
      return render_template("group.html",loggedin=False)
   
@app.route("/chat/",methods=['GET','POST'])
@app.route("/chat/<name>",methods=['GET','POST'])
def chat(name=None):
   ids= manager.getIDs()
   if 'username' in session:
      loggedin=True
      username=session['username']
      myGroups=manager.getUserGroups(username)
      notifs=manager.getNotifs(username)
      if request.method=='POST':
         if "submit" in request.form:
            if request.form["submit"] == "Go":
               print manager.getProfilePath()
               if manager.getProfilePath() != "profile/":
                  return redirect(manager.getProfilePath())
      chat = manager.getChat(name)
      return render_template("chat.html",loggedin=loggedin,ids=ids,chatlog=chat,name=name,username=username, myGroups=myGroups, notifs=notifs)
   return render_template("chat.html",loggedin=False)
      
@app.route("/login",methods=['GET','POST'])
def login():
   ids= manager.getIDs()
   if 'username' in session:
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() != "profile/":
               return redirect(manager.getProfilePath())
      luser = session['username']
      myGroups=manager.getUserGroups(luser)
      notifs=manager.getNotifs(luser)
      return render_template("login.html", loggedin=True, username=luser,ids=ids,myGroups=myGroups,notifs=notifs)

   if request.method=='POST':
      
      username = request.form['username']
      password = request.form['password']
      print 'Username and Password have been recorded as variables'
      
      exists = False
      loggedin = False
      reason = ""
      
      conn = sqlite3.connect("databases/users.db")
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
            if manager.getProfilePath() != "profile/":
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

         if email != repemail:
            registered=False
            reason = "Emails do not match"
            print "Emails do not match"

         if password == reppassword:
            registered=True
         else:
            registered=False
            reason = "Passwords do not match"
            print "Passwords do not match"


         conn = sqlite3.connect("databases/users.db")
         c = conn.cursor()
         
         c.execute("select * from uinfo")
         tabledata = c.fetchall()
         for d in tabledata:
            if username == d[0]:
               registered=False
               reason="The username "+username+" already exists!"
               print "Username % is already in use" %username
         
         pvalidate = manager.validateEntry(password)
         if pvalidate != "":
            registered=False
            reason = "Password: " + pvalidate
            
         uvalidate = manager.validateEntry(username)
         if uvalidate != "":
            registered=False
            reason = "Username: " + uvalidate
         
         if registered:
            insinfo="insert into uinfo values ('"+username+"','"+password+"','"+first+"','"+last+"','"+phone+"','"+email+"','"+facebook+"')"
            c.execute(insinfo)
            conn.commit()
            print 'Username and Password have been recorded as variables'
            manager.userNotifTable(username)
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
   conn = sqlite3.connect("databases/users.db")
   c = conn.cursor()
  
   if 'username' in session:
      loggedin=True
      username=session['username']
      if request.method=='POST':
         if request.form["submit"] == "Go":
            if manager.getProfilePath() != "profile/":
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
    
