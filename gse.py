from flask import Flask, redirect, request, render_template
from ezdb import TableDef, DatabaseDef
import sys

# Initialize DB
repotable = TableDef("redir")
repotable.AddField("hostname","text")
repotable.AddField("path","text")
repotable.AddField("url","text")

redirdb = DatabaseDef("db/redir.db")
redirdb.AddTable(repotable)

if not redirdb.Initialize():
  print "Error initializing database"
  sys.exit()

# Application

app = Flask(__name__)

@app.route("/")
def PerformDomainRedirect():
  hostname = request.headers.get("Host")
  
  if redirlist = redirdb.Select("redir",["hostname"],[hostname]):
    if thisredir = [a for a in redirlist where a["path"] == "/"]:
      return redirect(thisredir["url"])
    else:
      return render_template("error.html",message="Redirect for " + hostname + "/ not found")  
  else:
    return render_template("error.html",message="Hostname not defined")

@app.route("/<thisuri>")
def PerformRedirect(thisuri):
  hostname = request.headers.get("Host")

  return render_template("root-with-uri.html", hostname=hostname, uri=thisuri)

app.run(host="0.0.0.0",port=8080)  
