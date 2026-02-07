# Python SQLite Victory Log
This is Python program that captures a daily log of personal victories by date into an SQLite database. You can add victories, update victories, view all of the victories, view specific victories, view victories from a day or a date range and view statistics about victories.

## Instructions for Build and Use

[Software Demo](https://youtu.be/3KmU5W6ttFA)

Steps to build and/or run the software:

 1. Go to the official Python website https://www.python.org/downloads/ and click link to Download Python 3.10 or newer
 2. Then double-click the download installer, check the box that says Add Python to PATH, and click Install Now
 3. Install the Microsoft Python language support extension in VSCode to make the play button available
 4. Create a python file and import colorama with its needed functions at the top of the file
 5. In the terminal of VSCode go to the folder with the Python victory_log software
 6. Then to create a virtual environment so you can keep it local run the command: py -m venv venv 
 7. Then to activate the virtual environment, thereby keeping it local, enter the command: .\venv\Scripts\Activate.ps1
 8. Then install colorama with the command: pip install colorama

Instructions for using the software:

1. In VSCode go to the victory_log.py file in your project folder open the terminal at the bottom
2. If you are not in the folder for your project in the terminal use the cd command to get there
3. Activate the virtual environment by entering the command: .\venv\Scripts\Activate.ps1
4. Press the play button in the top right corner of the screen or enter the command: python victory_log.py
5. Use the provided menu in the terminal to work with the victory log
6. To exit the program enter 7 in the main menu

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Visual Studio Code
* Python 3.13.7 64-bit
* Virtual Environment (venv)
* Colorama
* Git / GitHub

## Useful Websites to Learn More

I found these websites useful in developing this software:

### Visual Studio Code :
* [Visual Studio Code & GitHub](https://code.visualstudio.com/docs/sourcecontrol/overview)
* 
### Python :
* [Python 3.11.1 Reference Manual](https://docs.python.org/3.11/)
* [Stack Overflow - How To Underline Text In Python 3.6.5](https://stackoverflow.com/questions/51001592/how-to-underline-text-in-python-3-6-5)
* [W3 Schools - Python String join() Method](https://www.w3schools.com/python/ref_string_join.asp)
* [How To Underline Text In Python?](https://copyassignment.com/how-to-underline-text-in-python/)
* [Python Cheat Sheet](https://labex.io/pythoncheatsheet/builtin/zip)

### Virtual Environment (venv) : 
* [How to Use Python's "py" Launcher for Windows](https://www.infoworld.com/article/3617292/how-to-use-pythons-py-launcher-for-windows.html )
* [Video - Using the "py" launcher with Python on Windows](https://www.youtube.com/watch?v=aBOdC5CrL1s&t=147s)
* [How to Setup Virtual Environments in Python](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/ )
* [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
* [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)

### Colorama : 
* [Colorama Download & Info](https://pypi.org/project/colorama/)
* [How to Print Colored Text in Python](https://www.studytonight.com/python-howtos/how-to-print-colored-text-in-python)

### SQLite : 
* [SQLite](https://www.pygame.org/wiki/GettingStarted](https://www.sqlitetutorial.net/ )
* [SQLite3](https://codingcampus.net/how-to-install-pygame-in-visual-studio-code/](https://docs.python.org/3.13/library/sqlite3.html )
* [SQLite Python](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
* [SQLite coalesce()](https://www.sqlitetutorial.net/sqlite-functions/sqlite-coalesce/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] I plan on adding Tkinter to this project so that it has a better user interface to add and update victories
* [ ] I plan on using Tkinter to be able to display the victories as well and statistics about them
* [ ] I plan on creating functions to be able to sort and find victories by common words
