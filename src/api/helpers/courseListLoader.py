import os
import json


def read():
    if os.path.exists('courseList.json'):
        with open('courseList.json', 'r') as f:
            course_list = json.load(f)
        return course_list
    else:
        return None
