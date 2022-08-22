import json

from src.parser.Parser import Parser
from src.model.CourseList import CourseList
from src.api.helpers import courseListLoader


def start_parse(working_semesters, use_async):
    course_list = CourseList()
    parser = Parser()
    parser.set_course_list(course_list)

    for current_semester in working_semesters:

        match current_semester:
            case 'fall':
                parser.set_semester('fall')
            case 'spring':
                parser.set_semester('spring')
            case 'summer':
                parser.set_semester('summer')

        if use_async:
            parser.parse_async()
        else:
            parser.parse_sync()

    course_list_json = json.dumps(parser.course_list, default=vars, indent=4, sort_keys=True)
    course_list_json_dict = json.loads(course_list_json)
    return course_list_json_dict


def update_course_list(course_list_dict, working_semesters):
    course_list_dict_old = courseListLoader.read()
    if course_list_dict_old is None:
        return course_list_dict

    for current_semester in working_semesters:
        match current_semester:
            case 'fall':
                course_list_dict_old['fall'] = course_list_dict['fall']
            case 'spring':
                course_list_dict_old['spring'] = course_list_dict['spring']
            case 'summer':
                course_list_dict_old['summer'] = course_list_dict['summer']
    return course_list_dict_old


def save_course_list_dict(course_list_dict):
    with open('courseList.json', 'w') as f:
        json.dump(course_list_dict, f)


def run(semester, use_async):
    if semester == 'all':
        working_semesters = ['fall', 'spring', 'summer']
    else:
        working_semesters = [semester]

    course_list_json_dict = start_parse(working_semesters, use_async)
    course_list_json_dict = update_course_list(course_list_json_dict, working_semesters)
    save_course_list_dict(course_list_json_dict)

    return course_list_json_dict


def main(semester, use_async):
    if semester is None:
        return

    run(semester, use_async)


if __name__ == '__main__':
    pass
