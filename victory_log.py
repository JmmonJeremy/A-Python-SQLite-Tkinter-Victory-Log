"""Project Outline"""
"""Database Operations""" #1 (INSERT INTO) inserting new data, #2 (UPDATE) modifying data, #3 (DELETE) deleting data, #4 (SELECT) retrieving data 
"""Database Tables""" #1 time_labels, #2 victories
"""Table Columns for victories""" #1 id, #2 victory, #3 number, #4 v_date #5 week_number 
"""Table Columns for time_labels""" #1 abbreviated_day, #2 full_day #3 day_number #4 week_number, #5 week_of_month #6months, #7 month_number #8 year
"""Stretch Challenge""" #1 Filter & find data by date #2 Use two aggregate functions to summarize numerical data #3 Use additional table & perform join
"""Python Operations""" #1 build the SQL commands, #2 submit those commands, #3 receive the results from the database, #4 use the results. 

"""CODE to IMPORT libraries used"""
import sqlite3
from datetime import date, datetime

"""CODE for resusable FUNCTIONS"""
# Returns the week number of the month using the majority-of-days rule.
def get_week_number(date_obj: datetime) -> int:
    """    
    Rule:
    - If the first weekday of the month is Thu(4), Fri(5), or Sat(6),
      that partial week belongs to the previous month.
    - Otherwise, it is Week 1.
    """
    # 0 = Sunday ... 6 = Saturday
    first_weekday = int(date_obj.replace(day=1).strftime('%w'))
    # Apply majority rule
    week1_offset = 0 if first_weekday <= 3 else 1
    # Add number how many days have passed in the 1st week since 1st of month
    # subtract 1 to make date_obj.day start at 0 like first_weekday does
    adjusted_day = (date_obj.day - 1) + first_weekday
    week_number = (adjusted_day // 7) + 1 - week1_offset # add 1 to start 0 based week at 1
    return week_number

"""CODE to CREATE & CONNECT to DATABASE"""
connection = sqlite3.connect("victory.db") # creates if doesn't exist & connects
cursor = connection.cursor() # extends sqlite3.Cursor

"""CODE to CREATE the time_labels TABLE"""
# Create static reference lookup table
cursor.execute("""
                CREATE TABLE IF NOT EXISTS time_labels (
                  abbreviated_day TEXT UNIQUE,
                  full_day TEXT UNIQUE,
                  day_number INTEGER UNIQUE,
                  week_number INTEGER UNIQUE,
                  week_of_month TEXT UNIQUE,
                  month TEXT UNIQUE,
                  month_number INTEGER UNIQUE,
                  year INTEGER UNIQUE
                )
              """)
"""CODE to CREATE insertion VARIABLES"""
# Pair day names with numbers for columns to correspond for joins using the date
day_data = [('Sun', 'Sunday', 0),
 ('Mon', 'Monday', 1),
 ('Tue', 'Tuesday', 2),
 ('Wed', 'Wednesday', 3),
 ('Thu', 'Thursday', 4),
 ('Fri', 'Friday', 5),
 ('Sat', 'Saturday', 6)]
# Pair week_of_month with week_number for columns to correspond for joins using the date & a formula
week_data = [(1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5')]
# Pair month names with numbers for joins - results in [('January', 1), ('February', 2), etc.] *number & name correspond in table
month_data = list(zip(
  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  [1,2,3,4,5,6,7,8,9,10,11,12]
))
# Input sources for year loop that inserts years 2026 to current year
start_year = 2026
current_year = datetime.now().year

"""CODE to INSERT data into time_labels TABLE"""
# Insert day text manual pairing to day numbers into time_labels - to use number for joins with date
cursor.executemany("INSERT OR IGNORE INTO time_labels (abbreviated_day, full_day, day_number) VALUES (?, ?, ?)", day_data)
# Insert week_numbers into time_labels using list
cursor.executemany("INSERT OR IGNORE INTO time_labels (week_number, week_of_month) VALUES (?, ?)", week_data)
# Insert months data into time_labels using pairing with zip - to use number for joins with date
cursor.executemany("INSERT OR IGNORE INTO time_labels (month, month_number) VALUES (?, ?)", month_data)
# Insert years into time_labels starting at 2026 and ending on current year using tuple, [year] would also work
for year in range(start_year, current_year + 1):
  cursor.execute("INSERT OR IGNORE INTO time_labels (year) VALUES (?)", (year,))
# Commit lookup inputs for time_labels table
connection.commit()

"""CODE to CREATE the victories TABLE"""
# Create victories table for holding a log of victories
cursor.execute("""
                CREATE TABLE IF NOT EXISTS victories (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  victory TEXT, 
                  number INTEGER CHECK(number >= 1),
                  v_date TEXT DEFAULT (date('now')),
                  week_number INTEGER
                )
              """)

"""CODE to CREATE the USER INTERFACE"""
# Create a menu with database operations - victories: #1 id, #2 victory, #3 number, #4 date
choice = None #INTERFACE#####################################################################################
while choice != 6:
  print("\nSelect an option:")
  print("1) Add a new victory")
  print("2) Edit a victory")
  print("3) Delete a victory")
  print("4) Show all victories")
  print("5) Show selected victory or victories")
  print("6) Exit")
  choice = int(input("->  "))
  print("   ‾‾‾")

  """CODE to PERFORM selected ACTIONS"""
  #CODE to INSERT or add a victory
  if choice == 1: #INSERT#######################################################################################
    # Have user enter their victory
    victory = input("Record your personal victory: ")
    # Have user enter a different date or use today's date
    today = date.today().isoformat() # 4 digit year - 2 digit month - 2 digit day
    entered_date = input(f"Enter date or press enter for default [{today}]: ")
    date_str = entered_date if entered_date else today
    # Compute the week_number the victory falls into
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    week_number = get_week_number(date_obj)
    # Have user enter a different date or use today's date
    cursor.execute("""
                    SELECT COALESCE(MAX(number), 0) + 1
                    FROM victories
                    WHERE v_date = ?
                  """, (date_str,))
    default_number = cursor.fetchone()[0]
    entered_number = input(f"Enter victory number or press enter for ordered number default [{default_number}]:")
    number = int(entered_number) if entered_number else default_number    
    # Make tuplet to insert victory into victories database
    values = (victory, number, date_str, week_number)
    cursor.execute("INSERT INTO victories (victory, number, v_date, week_number) VALUES (?, ?, ?, ?)", values)
    connection.commit()
    print(f"\nVictory number [{number}] on [{today}] of [{victory}] was successfully added to your log!")
  # CODE to UPDATE or edit a victory
  elif choice == 2: #UPDATE########################################################################################
    e_date = input("Enter the date of the victory to be edited: ")
    e_number = input("Enter the number of the victory to be edited: ")
    values = (e_date, int(e_number))
    cursor.execute("SELECT victory FROM victories WHERE v_date = ? AND number = ?", values)
    result = cursor.fetchone()
    e_victory = result[0] if result else None
    updated_number = input(f"Enter updated victory number or press enter for it to remain as [{e_number}]:")
    updated_number = updated_number if updated_number else e_number
    updated_victory = input(f"Enter updated victory or press enter for it to remain as [{e_victory}]:")
    updated_victory = updated_victory if updated_victory else e_victory
    updated_values = (int(updated_number), updated_victory, e_date, int(e_number))
    if result is None:
      print(f"\nERROR! The date [{e_date}] and number [{e_number}]  do not correspond to a victory, please try again.")
      continue 
    elif e_number != updated_number and e_victory != updated_victory:
      cursor.execute("UPDATE victories SET number = ?, victory = ? WHERE v_date = ? AND number = ?", updated_values)
      connection.commit()
      print(f"\nVictory number [{e_number}] on [{e_date}] of [{e_victory}] was successfully changed to #[{updated_number}] [{updated_victory}]!")
    elif e_number != updated_number and e_victory == updated_victory:
      cursor.execute("UPDATE victories SET number = ? WHERE v_date = ? AND number = ?", [int(updated_number), e_date, int(e_number)])
      connection.commit()
      print(f"\nVictory number [{e_number}] on [{e_date}] of [{e_victory}] was successfully changed to number [{updated_number}]!")
    elif e_number == updated_number and e_victory != updated_victory:
      cursor.execute("UPDATE victories SET victory = ? WHERE v_date = ? AND number = ?", (updated_victory, e_date, int(e_number)))
      connection.commit()
      print(f"\nVictory number [{e_number}] on [{e_date}] of [{e_victory}] was successfully changed to [{updated_victory}]!")
  # CODE to DELETE a victory
  elif choice == 3: #DELETE##########################################################################################
    d_date = input("Enter the date of the victory to be removed: ")
    d_number = int(input("Enter the number of the victory to be removed: "))
    values = (d_date, d_number)
    cursor.execute("SELECT victory FROM victories WHERE v_date = ? AND number = ?", values)
    result = cursor.fetchone()
    if result is None:
      print(f"\nERROR! The date [{d_date}] and number [{d_number}] do not correspond to an existing victory.") 
      continue
    else:
      d_victory = result[0]
      cursor.execute("DELETE FROM victories WHERE v_date = ? AND number = ?", values)
      connection.commit()    
      print(f"\nVictory [{d_number}] on [{d_date}] of [{d_victory}] was successfully deleted")
  # CODE to SELECT & show ALL victories
  elif choice == 4: #SELECT###########################################################################################
    cursor.execute("""
                    SELECT 
                      v.v_date,
                      m.month,
                      d.full_day,
                      w.week_of_month,
                      v.number,
                      v.victory
                    FROM victories v
                    LEFT JOIN time_labels d
                      ON d.day_number = CAST(strftime('%w', v.v_date) AS INTEGER)
                    LEFT JOIN time_labels m
                      ON m.month_number = CAST(strftime('%m', v.v_date) AS INTEGER)
                    LEFT JOIN time_labels w
                      ON w.week_number = v.week_number
                    ORDER BY v.v_date, v.number
                  """)
    print()
    for line in cursor.fetchall():
      # Unpack the tuple into separate variables instead of using indexing like line[0]
      date_str, month, day, week_of_month, number, victory = line
      # Build the composite column for the (month - week # - day) section
      date_info = f"({month} - {week_of_month} - {day})"      
      print(f"{date_str:<12} {date_info:<30}  {number:<3}  {victory}")
  # CODE to SELECT & show ALL victories
  elif choice == 5: #SELECT###########################################################################################
    print("\tSelect what you want to see:")
    print("\t1) Show a single victory")
    print("\t2) Show all victories for a day")
    print("\t3) Show all victories for a range of dates")
    selection = int(input("\t->  "))
    print("\t   ‾‾‾")
    if selection == 1:#SINGLE VICTORY#################################################################################
      s_date = input("Enter the date of the victory you want to see: ")
      s_number = int(input("Enter the number of the victory you want to see: "))
      values = (s_date, s_number)
      cursor.execute("SELECT victory FROM victories WHERE v_date = ? AND number = ?", values)
      result = cursor.fetchone()
      if result is None:
        print(f"\nERROR! The date [{s_date}] and number [{s_number}] do not correspond to an existing victory, please try again.") 
        continue
      else:
        cursor.execute("""
                        SELECT 
                          v.v_date,
                          m.month,
                          d.full_day,
                          w.week_of_month,
                          v.number,
                          v.victory
                        FROM victories v
                        LEFT JOIN time_labels d
                          ON d.day_number = CAST(strftime('%w', v.v_date) AS INTEGER)
                        LEFT JOIN time_labels m
                          ON m.month_number = CAST(strftime('%m', v.v_date) AS INTEGER)
                        LEFT JOIN time_labels w
                          ON w.week_number = v.week_number                        
                        WHERE v.v_date = ? AND v.number = ?
                      """, values)
        print()
        for line in cursor.fetchall():
          # Unpack the tuple into separate variables instead of using indexing like line[0]
          date_str, month, day, week_of_month, number, victory = line
          # Build the composite column for the (month - week # - day) section
          date_info = f"({month} - {week_of_month} - {day})"      
          print(f"{date_str:<12} {date_info:<30}  {number:<3}  {victory}")
    if selection == 2:#DAY'S VICTORIES#################################################################################
      sd_date = input("Enter the date of the victories you want to see: ")
      cursor.execute("SELECT victory FROM victories WHERE v_date = ?", (sd_date,))
      result = cursor.fetchone()
      if result is None:
        print(f"\nERROR! The date [{sd_date}] does not correspond to any existing victories, please try again.") 
        continue      
      cursor.execute("""
                      SELECT 
                        v.v_date,
                        m.month,
                        d.full_day,
                        w.week_of_month,
                        v.number,
                        v.victory
                      FROM victories v
                      LEFT JOIN time_labels d
                        ON d.day_number = CAST(strftime('%w', v.v_date) AS INTEGER)
                      LEFT JOIN time_labels m
                        ON m.month_number = CAST(strftime('%m', v.v_date) AS INTEGER)
                      LEFT JOIN time_labels w
                        ON w.week_number = v.week_number                        
                      WHERE v.v_date = ?
                    """, (sd_date,))
      print()
      for line in cursor.fetchall():
        # Unpack the tuple into separate variables instead of using indexing like line[0]
        date_str, month, day, week_of_month, number, victory = line
        # Build the composite column for the (month - week # - day) section
        date_info = f"({month} - {week_of_month} - {day})"      
        print(f"{date_str:<12} {date_info:<30}  {number:<3}  {victory}")
    if selection == 3:#RANGE OF VICTORIES#################################################################################
      begin_date = input("Enter the starting date of the victories you want to see: ")
      end_date = input("Enter the ending date for the victories you want to see: ")
      values = (begin_date, end_date)
      cursor.execute("SELECT victory FROM victories WHERE v_date >= ? AND v_date <= ?", values)
      result = cursor.fetchone()
      if result is None:
        print(f"\nERROR! There are not existing victories in the date range of [{begin_date} - {end_date}], please try again.") 
        continue
      cursor.execute("""
                        SELECT 
                          v.v_date,
                          m.month,
                          d.full_day,
                          w.week_of_month,
                          v.number,
                          v.victory
                        FROM victories v
                        LEFT JOIN time_labels d
                          ON d.day_number = CAST(strftime('%w', v.v_date) AS INTEGER)
                        LEFT JOIN time_labels m
                          ON m.month_number = CAST(strftime('%m', v.v_date) AS INTEGER)
                        LEFT JOIN time_labels w
                          ON w.week_number = v.week_number                        
                        WHERE v_date >= ? AND v_date <= ?
                      """, values)
      print()
      for line in cursor.fetchall():
        # Unpack the tuple into separate variables instead of using indexing like line[0]
        date_str, month, day, week_of_month, number, victory = line
        # Build the composite column for the (month - week # - day) section
        date_info = f"({month} - {week_of_month} - {day})"      
        print(f"{date_str:<12} {date_info:<30}  {number:<3}  {victory}")
# CODE to EXIT program
print("Way to log your efforts! See you next victory! Goodbye.")
connection.close()