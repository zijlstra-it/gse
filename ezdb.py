##########################################################
#
# ezdb.py - SQLite database functions
#
# NOTE: This only works with data of type text and varchar
#
# Import libraries
# from ezdb import TableDef, DatabaseDef
#
# Create a table object with fields:
# newtable = TableDef("people")
# newtable.AddFields("name","text")
# newtable.AddFields("age","text")
#
# Create database object
# newdb = DatabaseDef("db/test.db")
#
# Add table to database
# newdb.AddTable(newtable)
#
# Initialize database schema (write table schema to database)
# newdb.Initialize()
#
# Insert into table
#	SQL:  INSERT INTO people(name, age) VALUES("Bob","24");
# 	EZDB: newdb.Insert("people",["Bob","24"])i
#
#	Return True on success, False on failure
#
# Update table entry
# 	SQL:  UPDATE people SET name='Robert', age='26' WHERE name='Bob' AND age='24';
# 	EZDB: newdb.Update("people",["name","age"],["Robert","26"],["name","age"],["Bob","24"])
#	
#	returns True on success, False on failure
#
# Select Row(s) from table
#	SQL:  SELECT * FROM people WHERE name='Robert';
# 	EZDB: newdb.Select("people",["name"],["Robert"])
#
#	SQL:  SELECT * FROM people WHERE name='Robert' AND age='26';
# 	EZDB: newdb.Select("people",["name","age"],["Robert","26"])
#
#	returns [{"name": "Robert", "age":"26"}]
#	(additional rows will be pushed onto the array as additional dictonaries)
#
# Select all items from table
#	SQL:  SELECT * FROM people;
# 	EZDB: newdb.Select("people")
#
#       returns [{"name": "Robert", "age":"26"}]
#       (additional rows will be pushed onto the array as additional dictonaries)
#
##########################################################

import sqlite3
import os

class TableDef:
  def __init__(self,name):
    self.NAME = name
    self.FIELDS = []

  def AddField(self, name, type):
    self.FIELDS.append({ "name" : name, "type" : type })

  def Create(self):
    createlist = [a["name"] for a in self.FIELDS]
    if len(createlist) > 1:
      return str("CREATE TABLE " + self.NAME + "(" + ",".join(createlist) + ");")
    else:
      return False

  def Insert(self, valuelist):
    if len(valuelist) == len([a["name"] for a in self.FIELDS]):
      return str("INSERT INTO " + self.NAME + "(" + ",".join([a["name"] for a in self.FIELDS]) + ") VALUES('" + "','".join(valuelist) + "');")
    else:
      return False

  def Update(self, valuefieldlist, valuevaluelist, wherefieldlist, wherevaluelist):
    if len(valuefieldlist) == len(valuevaluelist) and len(wherefieldlist) == len(wherevaluelist):
      return str("UPDATE " + self.NAME + " SET " + ", ".join([valuefieldlist[idx] + "='" + valuevaluelist[idx] + "'" for idx in range(len(valuefieldlist))]) + " WHERE " + " AND ".join([wherefieldlist[idx] + "='" + wherevaluelist[idx] + "'" for idx in range(len(wherevaluelist))]) + ";")
    else:
      return False

  def Select(self, fieldlist, valuelist):
    if len([f for f in fieldlist if f in [a["name"] for a in self.FIELDS]]) > 0 and len(fieldlist) == len(valuelist):
      return str("SELECT * FROM " + self.NAME + " WHERE " + " AND ".join([fieldlist[idx] + "='" + valuelist[idx] + "'" for idx in range(len(fieldlist))]) + ";") 
    else:
      return False

  def SelectAll(self):
    return str("SELECT * FROM " + self.NAME + ";")

class DatabaseDef:
  def __init__(self, filename):
    self.DATABASE = filename
    self.TABLES = []

  def AddTable(self, tabledef):
    self.TABLES.append({"name" : tabledef.NAME, "obj" : tabledef })

  def ExistDB(self):
    return os.path.exists(self.DATABASE)

  def GetDB(self):
    return sqlite3.connect(self.DATABASE)

  def Initialize(self):
    try:
      if not self.ExistDB():
        db = self.GetDB()
        for table in self.TABLES:
          result = db.cursor().execute(table["obj"].Create())
        db.commit()
        db.close()
      return True
    except:
      return False

  def Insert(self, tablename, valuelist):
    try:
      db = self.GetDB()
      db.cursor().execute([a for a in self.TABLES if a["name"] == tablename][0]["obj"].Insert(valuelist))
      db.commit()
      db.close()
      return True
    except:
      return False

  def Update(self, tablename, valuefieldlist, valuevaluelist, wherefieldlist, wherevaluelist):
    try:
      db = self.GetDB()
      db.cursor().execute([a for a in self.TABLES if a["name"] == tablename][0]["obj"].Update(valuefieldlist,valuevaluelist,wherefieldlist,wherevaluelist))
      db.commit()
      db.close()
      return True
    except:
      return False

  def Select(self, tablename, fieldlist= None, valuelist = None):
    try:
      db = self.GetDB()
      returnval = None
      if fieldlist and valuelist:
        returnval = []
        result = db.cursor().execute([a for a in self.TABLES if a["name"] == tablename][0]["obj"].Select(fieldlist,valuelist)).fetchall()
        for thisresult in result:
          returnval.append(None)
          returnval[len(returnval)-1] = {}
          for i in range(0,len([a for a in self.TABLES if a["name"] == tablename][0]["obj"].FIELDS)):
            returnval[len(returnval)-1][[a for a in self.TABLES if a["name"] == tablename][0]["obj"].FIELDS[i]["name"]] = str(thisresult[i])
      else:
        returnval = []
        result = db.cursor().execute([a for a in self.TABLES if a["name"] == tablename][0]["obj"].SelectAll()).fetchall()
        for thisresult in result:
          returnval.append(None)
          returnval[len(returnval)-1] = {}
          for i in range(0,len([a for a in self.TABLES if a["name"] == tablename][0]["obj"].FIELDS)):
            returnval[len(returnval)-1][[a for a in self.TABLES if a["name"] == tablename][0]["obj"].FIELDS[i]["name"]] = str(thisresult[i])

      db.close()
      return returnval
    except:
      return False
