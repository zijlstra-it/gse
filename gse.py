from flask import Flask, redirect, request, render_template
from ezdb import TableDef, DatabaseDef
import sys, md5, random

def GetAuthToken(db):
  return str(db.Select("settings",["setname"],["authtoken"])[0]["setval"])

def GenerateAuthToken(db):
  tokenexist = db.Select("settings",["setname"],["authtoken"])
  if not tokenexist:
    hash = md5.new()
    hash.update(str(random.random()))
    authtoken = hash.hexdigest()
    
    if db.Insert("settings",["authtoken",authtoken]):
      f = open("./gse.conf","w")
      f.write("authtoken %s" % authtoken)
      f.close()
      return True
    else:
      return False

# Initialize DB and Application
redirtable = TableDef("redir")
redirtable.AddField("hostname","text")
redirtable.AddField("path","text")
redirtable.AddField("url","text")

settingstable = TableDef("settings")
settingstable.AddField("setname","text")
settingstable.AddField("setval","text")

redirdb = DatabaseDef("db/redir.db")
redirdb.AddTable(redirtable)
redirdb.AddTable(settingstable)

if not redirdb.Initialize():
  print "Error initializing database"
  sys.exit()

GenerateAuthToken(redirdb)
    

# Application

app = Flask(__name__)

@app.route("/", defaults ={'path':''}, methods=["GET","POST"])
@app.route("/<path:path>", methods=["GET","POST"])
def PerformRedirect(path):
  hostname = request.headers.get("Host")

  fulluri = "/" + path
  redirlist = redirdb.Select("redir",["hostname"],[hostname])
  if redirlist:
    thisredir = [a for a in redirlist if a["path"] == fulluri ]
    if thisredir:
      return redirect(thisredir[0]["url"])
    else:
      if request.method == "POST":
        if GetAuthToken(redirdb) == request.headers.get('GSE_authtoken'):
          redirdb.Insert("redir",[hostname,fulluri,str(request.headers.get('GSE_url'))])
          return redirect(str(request.headers.get('GSE_url')))
        else:
          return render_template("error.html",message="Incorrect Auth Token")
      else:
        return render_template("error.html",message="Redirect for " + hostname + fulluri + " not found")  
  else:
    if request.method == "POST":
      if GetAuthToken(redirdb) == request.headers.get('GSE_authtoken'):
        redirdb.Insert("redir",[hostname,fulluri,str(request.headers.get('GSE_url'))])
        return redirect(str(request.headers.get('GSE_url')))
      else:
        return render_template("error.html",message="Incorrect Auth Token")
    else:
      return render_template("error.html",message="Hostname (" + hostname + ") not defined")
 

app.run(host="0.0.0.0",port=8080)
