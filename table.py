
import os
import db

# Inserts a record into the table
def insertTuple(UserQuery, currDB, isLocked, u, c):
  tbInput = db.inputCleaner("insert into ", UserQuery)

  tbName = tbInput.split()[0] # Gets table name
  tbRest = tbInput.replace(tbName, "").replace(" values", "") #.replace('\t', "").replace(" ", "")
  tbAttrs0 = tbRest[1:] # Leaves only string with attributes
  tbAttrs1 = tbAttrs0[:-1] 
  tbAttrs = tbAttrs1.split(",") # Creates list from attributes
  tbAttrs[0] = tbAttrs[0].replace("(", "")

  

  def appendToFile():
    f = open(filename, 'a')
    f.write('\n')
    f.write(" | ".join(tbAttrs)) # Writes list to file with pipe delimiter
    f.close()

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
      if isLocked == 0:
        if u:
          os.system(f"cp {currDB}/{tbName}.txt {currDB}/{tbName}.new.txt")
          filename = currDB + '/' + tbName + '.new.txt'
          appendToFile()
          c.append(f"rm {currDB}/{tbName}.txt")
          c.append(f"mv {currDB}/{tbName}.new.txt {currDB}/{tbName}.txt")
        else:
          filename = currDB + '/' + tbName + '.txt'
          appendToFile()
        print(f"1 new record inserted into {tbName}.")
      else:
        print(f"Error: Table {tbName} is locked!")
    else:
      print(f"!Failed to add values to {tbName} because it does not exist.")
  else:
    print("Please select database to use.")



# Updates a record in the table
def updateTuple(UserQuery, currDB, isLocked, u, c):
  tbInput = db.inputCleaner("update ", UserQuery)

  tbName = tbInput.split()[0] # Gets table name
  setColumn = tbInput.split()[2] # Gets "set" column
  setRecord = tbInput.split()[4] #.replace("'", "") # Gets "set" record
  whereColumn = tbInput.split()[6] # Gets "where" column
  whereRecord = tbInput.split()[8] #.replace("'", "") # Gets "where" record

  def overwriteFile():
    f = open(filename, 'w')
    for line in tempFile:
      f.write(line)
    f.close()

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
      if isLocked == 0:
        filename = currDB + '/' + tbName + '.txt'

        f = open(filename, 'r')
        tempFile = f.readlines()
        f.close()

        count = 0
        mods = 0
        setColumnNum = 0
        whereColumnNum = 0
        for line in tempFile:
          if (count == 0): # Headers
            columnList = line.split()
            del columnList[1::3]
            setColumnNum = columnList.index(setColumn)
            whereColumnNum = columnList.index(whereColumn)
          if (count > 0): # Values
            tupleDetails = line.split()
            if (tupleDetails[whereColumnNum] == whereRecord):
            # Update data, Add newline if last column in row
              if ((setColumnNum+2) > len(tupleDetails)):
                tupleDetails[setColumnNum] = f'{setRecord}\n'
            # Update data
              else:
                tupleDetails[setColumnNum] = setRecord
              tempFile[count] = ' '.join(tupleDetails)
              mods += 1
          count += 1
      
        if u:
          filename = currDB + '/' + tbName + '.new.txt'
          os.system(f"touch {filename}")
          overwriteFile()
          c.append(f"rm {currDB}/{tbName}.txt")
          c.append(f"mv {currDB}/{tbName}.new.txt {currDB}/{tbName}.txt")
        else:
      # Overwriting the file
          os.system(f'truncate -s 0 {filename}.txt')
          overwriteFile()
        print(f"{mods} record(s) modified in {tbName}.")
      else:
        print(f"Error: Table {tbName} is locked!")
    else:
      print(f"!Failed to update values in {tbName} because it does not exist.")
  else:
    print("Please select database to use.")

# Removes a record from the table
def deleteTuple(UserQuery, currDB, isLocked, u, c):
  tbInput = db.inputCleaner("delete from ", UserQuery)

  tbName = tbInput.split()[0] # Gets table name
  whereColumn = tbInput.split()[2] # Gets "where" column
  whereRecord = tbInput.split()[4] #.replace("'", "") # Gets "where" record

  operand = db.getOperand(tbInput.split()[3])

  def overwriteFileWithDeletes():
    f = open(filename, 'w')
    for line in tempFile:
      if (line != None):
        f.write(line)
    f.close()

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
      if isLocked == 0:
        filename = currDB + '/' + tbName + '.txt'

      f = open(filename, 'r')
      tempFile = f.readlines()
      f.close()

      count = 0
      mods = 0
      whereColumnNum = 0
      for line in tempFile:
        if (count == 0): # Headers
          columnList = line.split()
          del columnList[1::3]
          whereColumnNum = columnList.index(whereColumn)
        if (count > 0): # Values
          tupleDetails = line.split()

          # Finds selected rows and deletes them
          def deleteTupleHelper(mods):
            if (operand == 0): # Equality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  tempFile[count] = None
                  mods += 1

              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  tempFile[count] = None
                  mods += 1

            elif (operand == 1): # Greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                tempFile[count] = None
                mods += 1

            elif (operand == -1): # Less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                tempFile[count] = None
                mods += 1

            return mods
          mods = deleteTupleHelper(mods)
        count += 1
      
        if u:
          filename = currDB + '/' + tbName + '.new.txt'
          os.system(f"touch {filename}")
          overwriteFileWithDeletes()
          c.append(f"rm {currDB}/{tbName}.txt")
          c.append(f"mv {currDB}/{tbName}.new.txt {currDB}/{tbName}.txt")
        else:
      # Overwrites the file
          os.system(f'truncate -s 0 {currDB}/{tbName}.txt')
          overwriteFileWithDeletes()       

        print(f"{mods} record(s) removed in {tbName}.")
      else:
        print(f"Error: Table {tbName} is locked!")
    else:
      print(f"!Failed to remove values in {tbName} because it does not exist.")
  else:
    print("Please select database to use.")