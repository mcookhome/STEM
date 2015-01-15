from flask import Flask, render_template, request, session,redirect,url_for
import sqlite3
import csv, unicodedata
import requests

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
    user=request.form["query"]
    path="profile/"+user
    return path

def sendEmail():
    print "xD"
    return requests.post(
        "https://api.mailgun.net/v2/sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org/messages",
        auth=("api", "key-65c16214d5cecd85f38bfd48f55b2ea3"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd754b0c61d9e423b927d1b46256add5a.mailgun.org>",
              "to": "William Tan <mcookhome@gmail.com>",
              "subject": "Hello matt",
              "text": "smd"}) 
