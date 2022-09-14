import json
import os
import asyncio
from absl import logging

import aiohttp

from src.parser.helpers import RequestMaker
from src.model.CourseList import CourseList, CourseListType
from src.model.Course import Course
from src.model.Section import Section
from src.parser.helpers import CourseListPageHelpers
from src.parser.helpers import ItemParser
from src.pattern.Pattern import local_fall_pattern, local_spring_pattern, local_summer_pattern


class Parser:
    settings = None

    mode: str
    semester: str
    max_page_num: int
    course_list: CourseListType
    course_dict: dict
    current_column_binding: dict

    @classmethod
    def load_default_settings(cls):
        with open('settings.json', 'r') as f:
            cls.settings = json.load(f)

    def __init__(self, mode='online'):
        self.mode = mode
        if not Parser.settings:
            Parser.load_default_settings()

    def set_course_list(self, course_list=None):
        if not course_list:
            self.course_list = CourseList()
        else:
            self.course_list = course_list

        return self.course_list

    def set_semester(self, semester):
        if semester not in Parser.settings['available_semesters']:
            raise Exception('Semester not available')
        if semester == 'fall':
            self.course_dict = self.course_list.fall
            self.current_column_binding = self.settings['columns']['fall']

        if semester == 'spring':
            self.course_dict = self.course_list.spring
            self.current_column_binding = self.settings['columns']['spring']

        if semester == 'summer':
            self.course_dict = self.course_list.summer
            self.current_column_binding = self.settings['columns']['summer']

        self.semester = semester

    def get_semester_url(self):
        if self.semester == 'fall':
            return Parser.settings['base_url_fall']

        if self.semester == 'spring':
            return Parser.settings['base_url_spring']

        if self.semester == 'summer':
            return Parser.settings['base_url_summer']

        raise Exception("Invalid semester or semester not set!")

    def get_local_max_page_num(self) -> int:
        results = os.listdir('src/html')
        max_num = 0

        if self.semester == 'fall':
            pattern = local_fall_pattern
        elif self.semester == 'spring':
            pattern = local_spring_pattern
        elif self.semester == 'summer':
            pattern = local_summer_pattern
        else:
            raise Exception("Invalid semester or semester not set!")

        for file_name in results:
            if res := pattern.match(file_name):
                max_num = max(max_num, int(res[1]))

        self.max_page_num = max_num
        return self.max_page_num

    def use_first_page_get_max_page_num(self) -> int:
        base_url = self.get_semester_url()
        first_page_url = base_url + '1'
        first_page_text = RequestMaker.get_html(first_page_url, headers=Parser.settings['headers'],
                                                verify=Parser.settings['verify'])
        first_page_soup = CourseListPageHelpers.make_soup(first_page_text, features='html.parser')
        self.max_page_num = CourseListPageHelpers.get_max_page(first_page_soup)
        return self.max_page_num

    def save_all_page(self) -> None:
        self.use_first_page_get_max_page_num()
        base_url = self.get_semester_url()
        for current_page_num in range(1, self.max_page_num + 1):
            page_url = base_url + str(current_page_num)
            current_page_text = RequestMaker.get_html(page_url, headers=self.settings['headers'],
                                                      verify=Parser.settings['verify'])
            RequestMaker.save_page(self.semester, current_page_num, current_page_text)

    def process_online_pages_sync(self):
        base_url = self.get_semester_url()
        for current_page_num in range(1, self.max_page_num + 1):
            page_url = base_url + str(current_page_num)
            current_page_text = RequestMaker.get_html(page_url, headers=self.settings['headers'],
                                                      verify=Parser.settings['verify'])
            self.process_page(current_page_text)

    async def process_online_pages_async(self):
        base_url = self.get_semester_url()
        tasks = []

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            for current_page_num in range(1, self.max_page_num + 1):
                page_url = base_url + str(current_page_num)
                tasks.append(asyncio.create_task(self.process_online_page_async(session, page_url)))

            await asyncio.wait(tasks)

    async def process_online_page_async(self, session, page_url):
        current_page_text = await RequestMaker.get_html_async(session, page_url, headers=self.settings['headers'])
        self.process_page(current_page_text)

    def process_offline_pages_sync(self):
        for current_page_num in range(1, self.max_page_num + 1):
            with open(f'src/html/{self.semester}_{current_page_num}.html', 'r') as f:
                text = f.read()
                self.process_page(text)

    def process_page(self, current_page_text):
        current_page_soup = CourseListPageHelpers.make_soup(current_page_text, features='html.parser')
        current_page_tbody = CourseListPageHelpers.get_tbody(current_page_soup)
        self.process_rows(CourseListPageHelpers.get_rows(current_page_tbody))

    def process_rows(self, rows):
        for row in rows:
            self.process_row(row)

    def process_row(self, row):
        tds = CourseListPageHelpers.get_cols(row)

        # logging.info("New row start!")

        courses = self.process_prefix(tds)
        course = self.process_suffix(tds, courses)
        section = self.process_section(tds, course)
        course_time_list = self.process_days_time_location(tds)
        self.process_course_time(course_time_list, section)

        # logging.info("New row end!")

    def process_prefix(self, tds):
        prefix, _ = ItemParser.parse_course(tds[self.current_column_binding['course']])

        # logging.info(f"prefix: {prefix}")

        if prefix not in self.course_dict:
            self.course_dict[prefix] = {}

        return self.course_dict[prefix]

    def process_suffix(self, tds, courses):
        _, suffix = ItemParser.parse_course(tds[self.current_column_binding['course']])


        # logging.info(f"suffix: {suffix} title: {title} cr: {cr}")

        if suffix not in courses:
            current_course = Course()
            courses[suffix] = current_course
        else:
            # if title != courses[suffix].title:
            #     raise Exception(f"Name does not match the existing one! {suffix} {title} {courses[suffix].title}")
            #
            # if cr != courses[suffix].cr:
            #     raise Exception(f"Cr does not match the existing one! {suffix} {title} {courses[suffix].title}")

            current_course = courses[suffix]

        return current_course

    def process_section(self, tds, course):
        section = ItemParser.parse_section(tds[self.current_column_binding['section']])
        title = ItemParser.parse_title(tds[self.current_column_binding['title']])
        cr = ItemParser.parse_cr(tds[self.current_column_binding['cr']])
        crn = ItemParser.parse_crn(tds[self.current_column_binding['crn']])
        info = ItemParser.parse_info(tds[self.current_column_binding['info']])
        notes = ItemParser.parse_notes(tds[self.current_column_binding['notes']])
        instructor, email = ItemParser.parse_instructor_and_email(tds[self.current_column_binding['instructor']])
        occupied, capacity = ItemParser.parse_cap(tds[self.current_column_binding['cap']])

        # logging.info(
        #     f"crn: {crn} info: {info} notes: {notes} instructor: {instructor} email: {email} cap[{occupied}, {capacity}]")

        if self.semester == 'summer':
            session = ItemParser.parse_session(tds[self.current_column_binding['session']])
            new_section = Section(crn, cr, title, info, notes, instructor, email, occupied, capacity, session=session)
        else:
            new_section = Section(crn, cr, title, info, notes, instructor, email, occupied, capacity)

        course.add_a_section(section, new_section)
        return new_section

    def process_days_time_location(self, tds):
        return ItemParser.parse_days_time_location(tds[self.current_column_binding['days']],
                                                   tds[self.current_column_binding['times']],
                                                   tds[self.current_column_binding['place']])

    def process_course_time(self, course_time_list, new_section):
        if not course_time_list:
            return

        for course_time in course_time_list:
            new_section.add_a_course_time(course_time)

    def parse_sync(self):
        if self.mode == 'online':
            self.use_first_page_get_max_page_num()
            self.process_online_pages_sync()
        elif self.mode == 'offline':
            self.get_local_max_page_num()
            self.process_offline_pages_sync()

    def parse_async(self):
        if self.mode == 'online':
            self.use_first_page_get_max_page_num()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.process_online_pages_async())
        elif self.mode == 'offline':
            self.get_local_max_page_num()
            self.process_offline_pages_sync()
