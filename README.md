# CS-457 Programming Assignment 3: Table Joins
# Build Environment
Mac OS
Visual Studio Code

python 3.8.2
# Executable & Compiling
To compile files: Type ' python3 -m main.py db.py query.py table.py ' into the terminal

To execute files: After compiling, the program should execute.

# Running The Program
After launching the executable, you should now be able to copy and paste each line from the sql file. Each expected output has been reach from my testing.

# Documentation/Notes
The system design is a simple design managing datable and tables.
My program has a simple way of organizing multiple databases by creating directories for them.
And multiple tables are handled by pushing them into a vector of table classes. 

My program now works in python with a tuple system to store items in a variable.
Directories is created and saved by storing the name of the database. Name of any database created is saved in the program and can be accessed for future uses.
After such, using a name directory, table is created by finding the name of the data and creating the table under the database filename. Data is parsed to pass in for use. And removing a table is done by using a simple remove function. 

Commands are turned into a list and parsed.
Table values are saved within index and place in a tuple similar to project 1 vector system. 
Once a command is parsed, data is formatted and appeneded to the end of the table text file. 
Select allows you to find the table index if it exists by looking through the tuple. 
Altering table is done similarily to select as it grabs the values in the table index, but differs by changing the values within the table index. Deleting a tuble requires a loop to iterate each line, once a specific data is found, the date is set to 'none'. 
Modifying a tuble is done similarily to deletion, but instead replaces the data that is found. Querying specific date is done by searching through the list for the right fields and creates a temporary list that stores each tuble as a string element in the list.

This program implemented design elements from PA 1 and PA 2. It included elements such like creating/deleting databases, as wellas to query and modify tables. It also allowed tables to be updated and queried effectively. The two joins were then implemented for this project in this revision as inner and left outer joins.

Inner joins takes a comparison and merge the tables based on the id given. 
The program reads the two tables and stores each line in Table_1 and Table_2 according to its intended use. Table names, values to compare, and their operands are parsed from the command's values. Table_Join, a new list, is made. A nested for-loop used by the join function compares the provided values from the command while iterating through both tables. These columns are not joined from either table if there is no correspondence for the given value. If the program notices there were no matches discovered for a value from Table_1, it will still insert that record with null information for Table_2's corresponding value. Left outer joins function precisely the same as inner joins.


The SQL file commands are slightly altered to make copying and pasting easier. The command .exit does not work as I only implemented .EXIT to function (fully capitalized).
Another thing to note is that my program has only been able to excute on Mac OS. I have not been able to execute the program on windows since project 2's development. 
