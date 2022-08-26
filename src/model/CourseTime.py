from src.pattern.Pattern import days_pattern, time_pattern


class CourseTime:

    @staticmethod
    def format_check(days: str, time: str) -> bool:

        if not days_pattern.match(days):
            return False

        if not time_pattern.match(time):
            return False

        return True

    @staticmethod
    def time_check(start: tuple[int, int], end: tuple[int, int]):
        if start[0] >= 24 or end[0] >= 24:
            return False

        if start[1] >= 60 or end[1] >= 60:
            return False

        return True

    @staticmethod
    def time_transform(time: str) -> tuple[tuple[int, int], tuple[int, int]]:
        start = (int(time[:2]), int(time[2:4]))
        end = (int(time[5:7]), int(time[7:9]))
        return start, end

    days: str or None
    start: tuple[int, int] or None
    end: tuple[int, int] or None
    place: str or None

    def __init__(self, days: str or None, time: str or None, place: str or None):
        if days and time:
            format_check_res = CourseTime.format_check(days, time)
            if not format_check_res:
                raise Exception(
                    f'Invalid CourseTime init day: {days} time: {time}')

        if days:
            self.days = days.upper()
        else:
            self.days = None

        if time:
            self.start, self.end = CourseTime.time_transform(time)
        else:
            self.start = None
            self.end = None

        if place:
            if len(place) == 2:
                self.place = place[0] + place[1]
            else:
                self.place = place
        else:
            self.place = None

        if time:
            time_check_res = CourseTime.time_check(self.start, self.end)
            if not time_check_res:
                raise Exception(f'Invalid CourseTime init time: {time}')

    def __lt__(self, __o):
        return self.time_string < __o.time_string
