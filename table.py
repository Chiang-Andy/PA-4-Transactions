
import os
import db

# Inserts a record into the table
def insertTuple(UserQuery, currDB):
  tbInput = db.inputCleaner("insert into ", UserQuery)

  tbName = tbInput.split()[0] # Gets table name
  tbRest = tbInput.replace(tbName, "").replace(" values", "") #.replace('\t', "").replace(" ", "")
  tbAttrs0 = tbRest[1:] # Leaves only string with attributes
  tbAttrs1 = tbAttrs0[:-1] 
  tbAttrs = tbAttrs1.split(",") # Creates list from attributes

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
      filename = currDB + '/' + tbName + '.txt'
      f = open(filename, 'a')
      f.write('\n')
      f.write(" |".join(tbAttrs)) # Writes list
      f.close()
      print(f"1 new record inserted into {tbName}.")
    else:
      print(f"!Failed to add values to {tbName} because it does not exist.")
  else:
    print("Please select database to use.")

# Updates a record in the table
def updateTuple(UserQuery, currDB):
  tInput = db.inputCleaner("update ", UserQuery)

  tbName = tInput.split()[0] # Gets table name
  setColumn = tInput.split()[2] # Gets "set" column
  setRecord = tInput.split()[4] #.replace("'", "") # Gets "set" record
  whereColumn = tInput.split()[6] # Gets "where" column
  whereRecord = tInput.split()[8] #.replace("'", "") # Gets "where" record

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
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
      
      # Overwriting the file
      os.system(f'truncate -s 0 {currDB}/{tbName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        f.write(line)
      f.close()

      print(f"{mods} record(s) modified in {tbName}.")
    else:
      print(f"!Failed to update values in {tbName} because it does not exist.")
  else:
    print("Please select database to use.")

# Removes a record from the table
def deleteTuple(UserQuery, currDB):
  tInput = db.inputCleaner("delete from ", UserQuery)

  tbName = tInput.split()[0] # Gets table name
  whereColumn = tInput.split()[2] # Gets "where" column
  whereRecord = tInput.split()[4] #.replace("'", "") # Gets "where" record

  operand = db.getOperand(tInput.split()[3])

  if (currDB != None):
    if db.tableCheck(tbName, currDB) == 1:
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
      
      # Overwrites the file
      os.system(f'truncate -s 0 {currDB}/{tbName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        if (line != None):
          f.write(line)
      f.close()

      print(f"{mods} record(s) removed in {tbName}.")
    else:
      print(f"!Failed to remove values in {tbName} because it does not exist.")
  else:
    print("Please select database to use.")