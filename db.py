
import os
import shlex
import subprocess

def inputCleaner(wordToRemove, UserQuery): # Removes ; and command
  query = UserQuery.replace(";", "")
  return query.replace(wordToRemove, "")

def databaseCheck(db): # Checks if database exists
  if db in subprocess.run(['ls', '|', 'grep', db], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def tableCheck(t, currDB): # Checks if table exists
  if t in subprocess.run(['ls', currDB,  '|', 'grep', t], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

# Determines operand and assigns value
def getOperand(o):
  operand = None
  if (o == '='):
    operand = 0
  elif (o == '<'):
    operand = -1
  elif (o == '>'):
    operand = 1
  elif (o == '!='):
    operand = -3
  return operand

def makeLock(currDB):
  if checkLock(currDB):
    return 0
  else:
    tablesToLock = subprocess.run(['ls', currDB, '|', 'grep ".txt"'], capture_output=True, text=True).stdout.split()
    tablesToLock.pop(0)
    for name in tablesToLock:
      os.system(f"touch {currDB}/{name}.lock")
    return 1

def checkLock(currDB):
  if ".lock" in subprocess.run(['ls', currDB, '|', 'grep ".lock"'], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def releaseLock(currDB, c):
  for cmd in c:
    os.system(cmd)
  os.system(f"rm {currDB}/*.lock")