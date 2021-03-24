# FloridaTechCourseListCrawler
A python crawler allows students to parse useful information from Florida Tech's course list

## Before Using
You need to have the following items installed in your computer to run this script
* Python 3
* Beautiful Soup 4 (Python Package)
* Requests (Python Package)
* xlwing (Python Package)
* Microsoft Excel

### Software Installation Quick Guide

#### Python 3
Go to [https://www.python.org/downloads/](https://www.python.org/downloads/) download the designated version for you device. Install Python by simply follow the instructions. Do not forget to add PATH for Python 3 interpreter.

#### Beautiful Soup 4 (Python Package)
Open your command line tool, PowerShell or cmd on Windows or terminal on MacOS, and type in ```pip install bs4```.

#### Requests (Python Package)
Similar to the process of installing Beautiful Soup 4. Please type in ```pip install requests``` in your command line.

#### xlwing (Python Package)
Also similar to the process of installing Beautiful Soup 4. Please type in ```pip install xlwing``` in your command line.

To check your package list, you can use ```pip list``` to get your list of the packages on your computer.

To remove a package, simply type in ```pip uninstall PACKAGE NAME```. Note that it's uninstall NOT remove. 

#### Microsoft Excel
Microsoft Office software package is available on its official website.

## Start Using
The steps are as follows:
1. Download the Python script inside src directory
1. Double check the url to the course list of Florida Tech.
1. Change the page range you want to parse
1. Comment out the columns you don't need
1. Run the script
1. Save the excel workbook (To save your memory space, the script will not let the workbook save automatically)

## Course List Excel Sheets
There are some already parsed course list excel sheets in the Course List directory. If you don't need the most recent number of registered student, you may download the excel file directly.
