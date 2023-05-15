
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