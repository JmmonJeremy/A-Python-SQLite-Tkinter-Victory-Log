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
# import re for regex expression check
import re
# import colorama to allow different colors for the hello text
import colorama
# import the functions to be used from colorama
from colorama import Fore, Back, Style

"""CODE for resusable FUNCTIONS"""
# Prompts for & returns a valid date input
def validate_date(prompt: str, allow_default=True) -> str:
  today_date = date.today()
  today_str = date.today().isoformat()
  while True:
    suffix = f" [{today_str}]" if allow_default else ""
    entered_date = input(f"{prompt}{suffix}: ").strip()
    # Allow default (press Enter)
    if entered_date == "" and allow_default:
      return today_str
    # Format check: YYYY-MM-DD
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entered_date):
      print("ERROR! Date must be in YYYY-MM-DD format (YYYY-MM-DD), please try again.")
      continue
    # Logical date check
    try:
      date_obj = datetime.strptime(entered_date, "%Y-%m-%d").date()
    except ValueError:
      print("ERROR! That is not a valid calendar date, please try again.")
      continue
    # Year constraint
    if date_obj.year < 2026:
      print("ERROR! Date cannot be before the year 2026, please try again.")
      continue
    # Future date check
    if date_obj > today_date:
      print("ERROR! Date cannot be after today, please try again.")
      continue
    # Passed all checks
    return date_obj.isoformat()

# Checks to make sure the 2nd date is after the first for a date range
def validate_end_date(prompt: str, start_date: str, allow_default=True) -> str:
  while True:
    entered_date = validate_date(prompt, allow_default=allow_default)
    if entered_date < start_date:
      print(f"ERROR! End date [{entered_date}] cannot be before the start date [{start_date}]. Please try again.")
      continue
    return entered_date
    
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

# Displays the requested victories
def show_victories(cursor, where_clause="", values=(), error_statement="", order_clause=""):
  cursor.execute(f"SELECT v.victory FROM victories v {where_clause}", values)
  result = cursor.fetchone()
  if result is None:
    print(f"\nERROR! {error_statement} please try again.") 
    return  
  cursor.execute(f"""
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
                  {where_clause}
                  {order_clause}
                """, values) 
  for line in cursor.fetchall():
    # Unpack the tuple into separate variables instead of using indexing like line[0]
    date_str, month, day, week_of_month, number, victory = line
    # Build the composite column for the (month - week # - day) section
    date_info = f"({month} - {week_of_month} - {day})"      
    print(f"{date_str:<11} {date_info:<58} Victory {number:<2} {victory}")

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
week_data = [(0, "Part of Previous Month's Last Week"), (1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5')]
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
while choice != 7:
  print("\nSelect an option:")
  print("1) Add a new victory")
  print("2) Edit a victory")
  print("3) Delete a victory")
  print("4) Show all victories")
  print("5) Show selected victory or victories")
  print("6) Look up statistics")
  print("7) Exit")
  choice = int(input("->  "))
  print("   ‾‾‾")

  """CODE to PERFORM selected ACTIONS"""
  #CODE to INSERT or add a victory
  if choice == 1: #INSERT#######################################################################################
    # Have user enter their victory
    victory = input("Record your personal victory: ")
    # Have user enter a different date or use today's date
    entered_date = validate_date(f"Enter date YYYY-MM-DD or press enter for the default of today's date")
    # Compute the week_number the victory falls into
    date_obj = datetime.strptime(entered_date, "%Y-%m-%d")
    week_number = get_week_number(date_obj)
    # Find and insert then correct number for the victory
    cursor.execute("""
                    SELECT COALESCE(MAX(number), 0) + 1
                    FROM victories
                    WHERE v_date = ?
                  """, (entered_date,))
    number = cursor.fetchone()[0]  
    # Make tuplet to insert victory into victories database
    values = (victory, number, entered_date, week_number)
    cursor.execute("INSERT INTO victories (victory, number, v_date, week_number) VALUES (?, ?, ?, ?)", values)
    connection.commit()
    print(f"\nVictory number [{number}] on [{entered_date}] of [{victory}] was successfully added to your log!")
  # CODE to UPDATE or edit a victory
  elif choice == 2: #UPDATE########################################################################################
    e_date = validate_date("Enter the date YYYY-MM-DD of the victory to be edited or press enter for the default of today's date")
    e_number = int(input("Enter the number of the victory to be edited: "))
    values = (e_date, e_number)
    cursor.execute("SELECT victory FROM victories WHERE v_date = ? AND number = ?", values)
    result = cursor.fetchone() 
    if result is None:
      print(f"\nERROR! The date [{e_date}] and number [{e_number}]  do not correspond to a victory, please try again.")
      continue  
    e_victory = result[0]  
    updated_victory = input(f"Enter updated victory or press enter for it to remain as [{e_victory}]:")
    updated_victory = updated_victory if updated_victory else e_victory
    updated_values = (updated_victory, e_date, e_number)    
    if e_victory != updated_victory:
      cursor.execute("UPDATE victories SET victory = ? WHERE v_date = ? AND number = ?", updated_values)
      connection.commit()
      print(f"\nVictory number [{e_number}] on [{e_date}] of [{e_victory}] was successfully changed to [{updated_victory}].")
    else:
      print(f"\nThere was no change made to victory number [{e_number}] on [{e_date}] of [{e_victory}].")
  # CODE to DELETE a victory
  elif choice == 3: #DELETE##########################################################################################
    d_date = validate_date("Enter the date YYYY-MM-DD of the victory to be removed or press enter for the default of today's date")
    d_number = int(input("Enter the number of the victory to be removed: "))
    values = (d_date, d_number)
    cursor.execute("SELECT victory FROM victories WHERE v_date = ? AND number = ?", values)
    result = cursor.fetchone()
    if result is None:
      print(f"\nERROR! The date [{d_date}] and number [{d_number}] do not correspond to an existing victory.") 
      continue
    d_victory = result[0]
    # Ask for confirmation before deleting
    confirm = input(f"\nAre you sure you want to delete victory [{d_number}] on [{d_date}] of [{d_victory}]? (y/n): ").strip().lower()
    if confirm != 'y':
      print("Deletion canceled.")
      continue
    cursor.execute("DELETE FROM victories WHERE v_date = ? AND number = ?", values)
    connection.commit()    
    print(f"\nVictory [{d_number}] on [{d_date}] of [{d_victory}] was successfully deleted")
  # CODE to SELECT & show ALL victories
  elif choice == 4: #SELECT###########################################################################################
    order_clause = "ORDER BY v.v_date, v.number"
    error_statement = "No victories exist to be displayed. First, record some victories, and then"
    show_victories(cursor, order_clause=order_clause, error_statement=error_statement)   
  # CODE to SELECT & specific victories
  elif choice == 5: #SELECT###########################################################################################
    print("   Select what you want to see:")
    print("   1) Show a single victory")
    print("   2) Show all victories for a day")
    print("   3) Show all victories for a range of dates")
    selection = int(input("   ->  "))
    print("      ‾‾‾")
    if selection == 1:#SINGLE VICTORY#################################################################################
      s_date = validate_date("Enter the date YYYY-MM-DD of the victory you want to see or press enter for the default of today's date")
      s_number = int(input("Enter the number of the victory you want to see: "))
      where_clause = "WHERE v.v_date = ? AND v.number = ?"
      values = (s_date, s_number)
      error_statement = f"The date [{s_date}] and number [{s_number}] do not correspond to an existing victory,"
      print() # Add empty line before output
      show_victories(cursor, where_clause, values, error_statement)      
    if selection == 2:#DAY'S VICTORIES################################################################################
      sd_date = validate_date("Enter the date YYYY-MM-DD of the victories you want to see or press enter for the default of today's date")     
      where_clause = "WHERE v.v_date = ?"
      value = (sd_date,)
      error_statement = f"The date [{sd_date}] does not correspond to any existing victories,"
      order_clause = "ORDER BY v.number"
      print() # Add empty line before output
      show_victories(cursor, where_clause, value, error_statement, order_clause)
    if selection == 3:#RANGE OF VICTORIES#############################################################################
      begin_date = validate_date("Enter the starting date YYYY-MM-DD of the victories you want to see", allow_default=False)
      end_date = validate_end_date("Enter the ending date YYYY-MM-DD for the victories you want to see or press enter for the default of today's date", begin_date)
      where_clause = "WHERE v.v_date >= ? AND v.v_date <= ?"
      values = (begin_date, end_date)
      error_statement = f"There are no existing victories in the date range of [{begin_date} - {end_date}],"
      order_clause = "ORDER BY v.v_date, v.number"
      print() # Add empty line before output
      show_victories(cursor, where_clause, values, error_statement, order_clause) 
  elif choice == 6: #AGGREGATE########################################################################################
    print("   Select what you want to see:")
    print("   1) Show total victory count for a day")
    print("   2) Show total victory count for a week, month, etc")
    print("   3) Show the lowest, highest, and average victory count for a range of dates")    
    option = int(input("   ->  "))    
    if option == 1:#COUNT FOR DAY##################################################################################
      ct_date = validate_date("Enter the date YYYY-MM-DD you want to see a victory total for or press enter for the default of today's date")
      cursor.execute("SELECT COUNT(*) FROM victories WHERE v_date = ?", (ct_date,))
      victory_tot = cursor.fetchone()[0]
      print() # Add empty line before output
      print(Fore.MAGENTA + f"{ct_date} Total Victory Count: " + Fore.YELLOW + f"\033[4m {victory_tot} \033[0m" + Style.RESET_ALL)
    if option == 2:#COUNT FOR RANGE##################################################################################
      begin_ct_date = validate_date("Enter the start date YYYY-MM-DD for the time period you want to see a victory total for", allow_default=False)
      end_ct_date = validate_end_date("Enter the end date YYYY-MM-DD for the time period you want to see a victory total for or press enter for the default of today's date", begin_ct_date)
      values = (begin_ct_date, end_ct_date)
      cursor.execute("SELECT COUNT(*) FROM victories WHERE v_date BETWEEN ? AND ?", values)
      victory_tot = cursor.fetchone()[0]
      print() # Add empty line before output
      print(Fore.MAGENTA + f"{begin_ct_date} to {end_ct_date} Total Victory Count: " + Fore.YELLOW + f"\033[4m {victory_tot} \033[0m" + Style.RESET_ALL)
    if option == 3:#MIN, MAX, AVG FOR RANGE##################################################################################
      begin_calc_date = validate_date("Enter the start date YYYY-MM-DD for the time period you want to see a victory low, high, & average for", allow_default=False)
      end_calc_date = validate_end_date("Enter the end date YYYY-MM-DD for the time period you want to see a victory low, high, & average for or press enter for the default of today's date", begin_calc_date)
      values = (begin_calc_date, end_calc_date)
      cursor.execute("SELECT COUNT(*) FROM victories WHERE v_date BETWEEN ? AND ?", values)
      victory_low = cursor.fetchone()[0]
      victory_high = ""
      victory_ave = ""
      cursor.execute("""
                      SELECT
                        MIN(daily_count),
                        MAX(daily_count),
                        AVG(daily_count)
                      FROM (
                        SELECT v_date, COUNT(*) AS daily_count
                        FROM victories
                        WHERE v_date BETWEEN ? AND ?
                        GROUP BY v_date
                      )
                    """, (begin_calc_date, end_calc_date))

      victory_low, victory_high, victory_ave = cursor.fetchone()
      print() # Add empty line before output
      print(Fore.MAGENTA + f"{begin_calc_date} to {end_calc_date} Victory \033[4mLow\033[0m, " + Fore.MAGENTA + f"\033[4mHigh\033[0m, " + Fore.MAGENTA + f"\033[4mAverage\033[0m: " + Fore.YELLOW + f"\033[4m {victory_low} \033[0m , " + Fore.YELLOW + f"\033[4m {victory_high} \033[0m , " + Fore.YELLOW + f"\033[4m {victory_ave} \033[0m" + Style.RESET_ALL)
# CODE to EXIT program
print("Way to log your efforts! See you next victory! Goodbye.")
connection.close()