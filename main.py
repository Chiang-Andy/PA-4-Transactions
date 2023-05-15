# Andy Chiang
# database Project 2
# Main driver file

import os

import db
import table
import query
import join

currDB = None
UserQuery = None
TableList = [None]

while (UserQuery != ".EXIT"):
  UserQuery = input(">> ")
  if (';' not in UserQuery and UserQuery != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database
  elif ("CREATE DATABASE" in UserQuery.upper()):
    dbName = db.inputCleaner("CREATE DATABASE ", UserQuery)
    if db.databaseCheck(dbName) == 0:
      os.system(f'mkdir {dbName}')
      print(f"Database  {dbName} created.")
    else:
      print(f"!Failed to create database {dbName} because it already exists.")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery.upper()):
    dbName = db.inputCleaner("DROP DATABASE ", UserQuery)
    if db.databaseCheck(dbName):
      os.system(f'rm -r {dbName}')
      print(f"Database {dbName} deleted.")
    else:
      print(f"!Failed to delete {dbName} because it does not exist.")
  
  # Use database
  elif ("USE" in UserQuery.upper()):
    currDB = db.inputCleaner("USE ", UserQuery)
    #os.system('cd ' + currDB)
    if db.databaseCheck(currDB):
      print(f"Using database {currDB}.")
    else:
      print(f"!Failed to use {currDB} because it does not exist.")

  # Creates table 
  elif ("CREATE TABLE" in UserQuery.upper()):
    # Splits input into separate strings
    tbInput = db.inputCleaner("CREATE TABLE ", UserQuery).replace("create table ", "")
    tbName = tbInput.split()[0] # Grabs table name
    tbRest = tbInput.replace(tbName, "")
    tbAttrs0 = tbRest[2:] 
    tbAttrs1 = tbAttrs0[:-1] 
    tbAttrs = tbAttrs1.split(",") # Creates list from attributes

    if (currDB != None):
      if db.tableCheck(tbName, currDB) == 0:
        os.system(f'touch {currDB}/{tbName}.txt')
        filename = currDB + '/' + tbName + '.txt'
        f = open(filename, 'w')
        f.write(" |".join(tbAttrs)) # Writes list to file
        f.close()
        print(f"Table {tbName} created.")
      else:
        print(f"!Failed to create {tbName} because it already exists.")
    else:
      print("Please select database to use.")

  # Deletes table
  elif ("DROP TABLE" in UserQuery.upper()):
    tbName = db.inputCleaner("DROP TABLE ", UserQuery)
    if (currDB != None):
      if db.tableCheck(tbName, currDB):
        os.system(f'rm {currDB}/{tbName}.txt')
        print(f"Table {tbName} deleted from database {currDB}.")
      else:
        print(f"!Failed to delete {tbName} because it does not exist.")
    else:
      print("Please select database to use.")
  
  # Returns table elements as selected
  elif ("SELECT" in UserQuery.upper()):
    if ("SELECT *" in UserQuery.upper()):
      if ("." in UserQuery.upper()):
          join.joinTableOpener(UserQuery, currDB)
      else:
        query.queryAll(UserQuery, currDB)
    else:
      query.querySelect(UserQuery, currDB)

  # Modifies table by adding attribute
  elif ("ALTER TABLE" in UserQuery.upper()):
    alter = db.inputCleaner("ALTER TABLE ", UserQuery)
    tbName = alter.split()[0] # Grabs table name
    alterCmd = alter.split()[1] # Grabs command (ADD, etc)
    alterRest1 = alter.replace(tbName, "")
    alterRest2 = alterRest1.replace(alterCmd, "") # Left with attributes
    newAttr = alterRest2[2:] 

    if currDB != None:
      if db.tableCheck(tbName, currDB):
        f = open(f'{currDB}/{tbName}.txt', 'a')
        f.write(f" | {newAttr}") # Appends attribute to file with pipe delimiter
        f.close()
        print(f"Table {tbName} modified.")
      else:
        print(f"!Failed to modify table {tbName} because it does not exist.")
    else:
      print("Please select database to use.")
  
  elif ("INSERT INTO" in UserQuery.upper()):
    table.insertTuple(UserQuery, currDB)
  
  elif ("UPDATE" in UserQuery.upper()):
    table.updateTuple(UserQuery, currDB)
  
  elif ("DELETE FROM" in UserQuery.upper()):
    table.deleteTuple(UserQuery, currDB)
  
  elif (".EXIT" != UserQuery):
    print("I don't know what you want me to do.")

quit()