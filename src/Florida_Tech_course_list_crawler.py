'''
This script is used to parse information from Florida Tech's course list
'''

from bs4 import BeautifulSoup
import requests
import xlwings as xw

#create a Excel workbook and a worksheet
wb = xw.Book()
ws = wb.sheets[0]

#initiate the row number
excel_row_num = 1

'''
Change the range to mach the pages you want to parse
Since there might be a ssl problem with the requests module, we added verify=False to bypass the ssl verification
'''
#course table ranges from page1 to page50
for page in range(1,51):

    #get the webpage source and pass it to beautifulsoup
    source = requests.get(f'https://apps.fit.edu/schedule/main-campus/fall?query=&page={page}', verify=False).text
    soup = BeautifulSoup(source, features= 'lxml')

    #target the course table
    course_table = soup.find('table', {'id' : 'course-table'})
    course_table_contents = course_table.find('tbody')

    #all tows in that page
    all_rows = course_table_contents.find_all('tr')
    
    #find each item in each row (a course)
    for each_row in all_rows:

        #find all items in that row
        table_td = each_row.find_all('td')

        #get CRN
        course_item_CRN = table_td[0].text
        print(course_item_CRN)
        ws.cells(excel_row_num, 1).value = course_item_CRN

        #get course and split
        course_item_course = table_td[1].text
        course_item_course = course_item_course.split(' ')
        print(course_item_course)
        ws.cells(excel_row_num, 2).value = course_item_course[0]
        ws.cells(excel_row_num, 3).value = course_item_course[1]

        #get section number
        course_item_section = table_td[2].text
        print(course_item_section)
        ws.cells(excel_row_num, 4).value = course_item_section

        #get credits number
        course_item_credits = table_td[3].text
        print(course_item_credits)
        ws.cells(excel_row_num, 5).value = course_item_credits

        #get course title and course description (find prerequisites)
        course_item_title = table_td[4]
        course_span = course_item_title.find('span')
        course_title = course_span.text
        
        if course_title[0] == ' ':
            course_title = course_title.replace(' ', '', 1)

        course_description = course_span.get('data-content')

        if 'Prerequisites: ' in course_description:
            prerequisites = course_description.split('Prerequisites: ')[-1]
            prerequisites = prerequisites[:-1]  #get rid of ')'
            prerequisites_list = prerequisites.replace(', ', '\n')  #not a list object

        else:
            prerequisites_list = 'Not specified in the description'

        print(course_title)
        ws.cells(excel_row_num, 6).value = course_title

        print(course_description)
        ws.cells(excel_row_num, 7).value = course_description

        print(prerequisites_list)
        ws.cells(excel_row_num, 8).value = prerequisites_list       #not a list object

        #get notes
        course_item_notes = table_td[5].text

        if course_item_notes == '':
            course_item_notes = 'None'

        print(course_item_notes)
        ws.cells(excel_row_num, 9).value = course_item_notes

        #get days
        course_item_days = table_td[6].text
        course_item_days = course_item_days.replace(' ', '').replace('\n', '', 1)
        course_item_days = course_item_days[:-1]

        if course_item_days == '':
            course_item_days = 'None'

        print(course_item_days)
        ws.cells(excel_row_num, 10).value = course_item_days

        #get times
        course_item_times = table_td[7].text
        course_item_times = course_item_times.replace(' ', '').replace('\n', '', 1)
        course_item_times = course_item_times[:-1]

        if course_item_times == '':
            course_item_times = 'None'

        print(course_item_times)
        ws.cells(excel_row_num, 11).value = course_item_times

        #get place
        course_item_place = table_td[8].text
        course_item_place = course_item_place.replace(' ', '').replace('\n', '', 1)
        course_item_place = course_item_place[:-1]

        if course_item_place == '':
            course_item_place = 'None'

        print(course_item_place)
        ws.cells(excel_row_num, 12).value = course_item_place

        #get instructor & instructor's e-mial
        course_item_instructor = table_td[9]

        if 'TBA' in course_item_instructor.text:
            instructor_name = 'TBA'
            instructor_email = 'None'
        else:
            course_instructor = course_item_instructor.find('a')
            if course_instructor is None:
                instructor_email = 'None'
                instructor_name = 'None'
            else:
                instructor_email = course_instructor.get('href').replace('mailto:', '')
                instructor_name = course_instructor.text

        print(instructor_name)
        ws.cells(excel_row_num, 13).value = instructor_name
        print(instructor_email)
        ws.cells(excel_row_num, 14).value = instructor_email

        #get cap
        course_item_cap = table_td[10].text
        course_cap = course_item_cap.split('/')

        print(course_cap)
        ws.cells(excel_row_num, 15).value = course_cap[0]
        ws.cells(excel_row_num, 16).value = course_cap[1]

        #set the row number to next
        excel_row_num += 1

