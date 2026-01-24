# Class Tutorial Video Help
"""
CREATE TABLE IF NOT EXISTS table (column1 TEXT, column2 INTEGER, colum3 REAL, ...)
SELECT columns FROM table WHERE condition ORDER BY column ASC|DESC
INSERT INTO table VALUES (value1, value2, ...)
UPDATE table SET column = value WHERE condition
DELETE FROM table WHERE condition
"""
import sqlite3

connection = sqlite3.connect("books.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, pages INTEGER, read INTEGER)")

choice = None
while choice != 5:
  print("Select an option:")
  print("1) Add a new book")
  print("2) Delete a book")
  print("3) Show all Books")
  print("4) Read a book")
  print("5) Exit")
  choice = int(input("> "))
  if choice == 1:
    title = input("Enter book name: ")
    pages = int(input("Enter number of pages: "))
    read = 0
    values = (title, pages, read)
    cursor.execute("INSERT INTO books VALUES (?, ?, ?)", values)
    connection.commit()
  elif choice == 2:
    title = input("Enter the book to remove: ")
    values = (title,)
    cursor.execute("DELETE FROM books WHERE title = ?", values)
    connection.commit()
    if cursor.rowcount == 0:
      print("ERROR! Book does not exist")    
  elif choice == 3:
    cursor.execute("SELECT * from books ORDER BY title")
    for record in cursor.fetchall():
      print(f"{record[0]}\t{record[1]}\t{record[2]}")
  elif choice == 4:
    cursor.execute("SELECT title, read FROM books ORDER BY title")
    records = cursor.fetchall()
    for index in range(len(records)):
      print(f"{index+1} {records[index][0]}")
    choice = int(input("> "))
    selected_title = records[choice-1][0]
    values = (records[choice-1][1] + 1, selected_title)
    cursor.execute("UPDATE books SET read = ? WHERE title = ?", values)
    connection.commit()
print("Goodbye")
connection.close()