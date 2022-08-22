from src.model.CourseTime import CourseTime
from src.pattern.Pattern import course_pattern, days_pattern, times_pattern, location_pattern, \
    email_pattern


def parse_crn(item) -> str:
    return item.text


def parse_course(item) -> tuple[str, str]:
    text = item.text
    course_res = course_pattern.match(text)

    try:
        a = course_res[1]
        b = course_res[2]
    except:
        print(text)
        print(course_res[1], course_res[2])
    return course_res[1], course_res[2]


def parse_section(item) -> str:
    return item.text


def parse_cr(item) -> list[float, float]:
    cr = item.text.strip()

    if '.' in cr and '_' not in cr:
        return [float(cr), float(cr)]

    if len(cr) == 1:
        return [float(cr), float(cr)]

    cr = cr.split('-')
    cr_low = float(cr[0])
    cr_high = float(cr[1])
    return [cr_low, cr_high]


def parse_info(item) -> str:
    return item.find('span').get('data-content')


def parse_title(item) -> str:
    return item.text.strip()


def parse_notes(item) -> str or None:
    if len(item.text) == 0:
        return None
    return item.text


def parse_days_time_location(item_days, item_times, item_location):
    day_list = days_pattern.findall(item_days.text)
    time_list = times_pattern.findall(item_times.text)
    location_list = location_pattern.findall(item_location.text)

    output = []
    max_length = max(len(day_list), int(len(location_list) / 2))

    for index in range(max_length):
        try:
            days = day_list[index]
        except IndexError:
            days = None

        try:
            time = time_list[index]
        except IndexError:
            time = None

        try:
            location = [location_list[index * 2], location_list[index * 2 + 1]]
        except IndexError:
            location = None

        if days:
            for day in range(len(days)):
                output.append(CourseTime(days[day], time, location))

        elif time or location:
            output.append(CourseTime(days, time, location))

    return output


def parse_instructor_and_email(item) -> list[str, str]:
    instructor_name = item.text.strip()
    a_tag = item.find('a')
    if a_tag:
        raw_email = a_tag.get('href')
        email = email_pattern.search(raw_email)[0]
    else:
        email = None

    return [instructor_name, email]


def parse_session(item) -> str or None:
    text = item.text
    if len(text) > 0:
        return text

    return None


def parse_cap(item) -> list[str, str]:
    return item.text.split('/')
