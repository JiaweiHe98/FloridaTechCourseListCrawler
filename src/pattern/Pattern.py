import re

crn_pattern = re.compile(r'\d+')
course_pattern = re.compile(r'^([A-Z]{3,4})\s(\d{1,4})$')
prefix_pattern = re.compile(r'[A-Z]{3,4}')
suffix_pattern = re.compile(r'\d{3}')
days_pattern = re.compile(r'[MTWRFSU]+')
times_pattern = re.compile(r'\d{4}-\d{4}')
location_pattern = re.compile(r'\w+')
email_pattern = re.compile(r'(\w+@fit\.edu|\w+@my.fit\.edu)')
day_pattern = re.compile(r'[MTWRFSU]')
time_pattern = re.compile(r'\d{4}-\d{4}')


local_fall_pattern = re.compile(r'fall_(\d+)\.html')
local_spring_pattern = re.compile(r'spring_(\d+)\.html')
local_summer_pattern = re.compile(r'summer_(\d+)\.html')
