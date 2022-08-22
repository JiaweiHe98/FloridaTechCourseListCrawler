from src.pattern.Pattern import prefix_pattern
from typing import Protocol


class CourseListType(Protocol):
    fall: dict
    spring: dict
    summer: dict


class CourseList:

    @staticmethod
    def check_prefix(prefix):
        if not prefix_pattern.match(prefix):
            return False

    @staticmethod
    def first_time_add_initializer(semester_dict, prefix):
        if prefix in semester_dict:
            return

        semester_dict[prefix] = []

    all_semester = ('fall', 'spring', 'summer')

    fall: dict[str, list]
    spring: dict[str, list]
    summer: dict[str, list]

    def __init__(self):
        self.fall = {}
        self.spring = {}
        self.summer = {}

    def add_a_course(self, semester, prefix, course):
        if semester not in CourseList.all_semester:
            raise Exception(f'Invalid semester {semester}')

        if not CourseList.check_prefix(prefix):
            raise Exception(f'Invalid prefix {prefix}')

        if semester == 'fall':
            CourseList.first_time_add_initializer(self.fall, prefix)
            self.fall[prefix].append(course)

        elif semester == 'spring':
            CourseList.first_time_add_initializer(self.spring, prefix)
            self.spring[prefix].append(course)

        else:
            CourseList.first_time_add_initializer(self.summer, prefix)
            self.summer[prefix].append(course)
