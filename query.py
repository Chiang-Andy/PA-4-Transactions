

import os
import db

# Select *
def queryAll(UserQuery, currDB):
  selLower = db.inputCleaner("SELECT * FROM ", UserQuery)
  selection = db.inputCleaner("select * from ", selLower)
  if currDB != None:
    if db.tableCheck(selection, currDB):
      f = open(f'{currDB}/{selection}.txt', 'r')
      print(f.read())
      f.close()
    else:
      print(f"!Failed to query table {selection} because it does not exist.")
  else:
    print("Please select database to use.")

# Select (with variables)
def querySelect(UserQuery, currDB):
  selLower = db.inputCleaner("SELECT ", UserQuery)
  selection = db.inputCleaner("select ", selLower)

  # list of variables
  selectColumns = selection.replace(",", "").split()
  selectColumns = selectColumns[:selectColumns.index("from")]

  # Table name
  tbName = selection.split()[len(selectColumns)+1]

  # filter
  whereColumn = selection.split()[len(selectColumns)+3]
  whereRecord = selection.split()[len(selectColumns)+5]
  operand = db.getOperand(selection.split()[len(selectColumns)+4])

  if currDB != None:
    if db.tableCheck(tbName, currDB):
      f = open(f'{currDB}/{tbName}.txt', 'r')
      tempFile = f.readlines()
      f.close()

      selectColumnNums = []
      columnNameString = ""
      listToReturn = []
      count = 0
      for line in tempFile:
        if (count == 0): 
          # Finding the indexes of select and where columns
          columnList = line.split()
          columnListWithTypes = columnList.copy()
          del columnListWithTypes[2::3]

          del columnList[1::3]
          columnCount = 0

          # If variable is found in table, record index
          for word in columnList:
            if word in selectColumns:
              selectColumnNums.append(columnCount)
            if (word == whereColumn):
              whereColumnNum = columnCount
            columnCount += 1

          # Creating table header for the selected columns
          for index in selectColumnNums:
            columnNameString += f"{columnListWithTypes[index]} {columnListWithTypes[index+1]} | "
          queryHeader = columnNameString[:-3]
          listToReturn.append(queryHeader)

        if (count > 0): # Values
          tupleDetails = line.split()

          # Determines what to do with each row
          def querySelectHelper():

            # Creates the row output
            def queryStringMaker():
              queryString = ""
              for index in selectColumnNums:
                queryString += f"{tupleDetails[index]} | "
              queryResult = queryString[:-3]
              listToReturn.append(queryResult)

            if (operand == 0): # Equal
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  queryStringMaker()

            elif (operand == 1): # Greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                queryStringMaker()

            elif (operand == -1): # Less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                queryStringMaker()

            elif (operand == -3): # Inequality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] != whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) != float(whereRecord)):
                  queryStringMaker()

          querySelectHelper()

        count += 1
      for line in listToReturn: # Prints table
        print(line)

    else:
      print(f"!Failed to query table {tbName} because it does not exist.")
  else:
    print("Please select database to use.")