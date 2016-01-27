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

@app.route("/", defaults ={'path':''})
@app.route("/<path:path>")
def PerformRedirect(path):
  hostname = request.headers.get("Host")

  fulluri = "/" + path
  redirlist = redirdb.Select("redir",["hostname"],[hostname])
  if redirlist:
    thisredir = [a for a in redirlist if a["path"] == fulluri ]
    if thisredir:
      return redirect(thisredir[0]["url"])
    else:
      return render_template("error.html",message="Redirect for " + hostname + fulluri + " not found")  
  else:
    return render_template("error.html",message="Hostname not defined")
 


  return render_template("root-with-uri.html", hostname=hostname, uri=thisuri)

app.run(host="0.0.0.0",port=8080)  
