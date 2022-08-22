from src.pattern.Pattern import email_pattern


class Section:

    @staticmethod
    def format_check(crn: str, email: str):
        if len(crn) != 5:
            return False

        if not email:
            return True

        if not email_pattern.match(email):
            return False

        return True

    @staticmethod
    def check_closed(occupied, capacity):
        occupied = int(occupied)
        capacity = int(capacity)

        if capacity < occupied:
            return True
        return False

    crn: int
    cr: list[float, float]
    title: str
    info: str
    notes: str or None
    session: str or None
    time: list[object]
    instructor: str
    email: str
    occupied: int
    capacity: int
    closed: bool

    def __init__(self, crn: str, cr: list[float, float], title: str, info: str, notes: str, instructor: str, email: str,
                 occupied: str, capacity: str, session=None):
        format_check_res = self.format_check(crn, email)
        if not format_check_res:
            raise Exception(
                f'Cannot init section crn: {crn} email: {email} occupied: {occupied} capacity: {capacity}')

        self.crn = int(crn)
        self.cr = cr
        self.title = title
        self.info = info
        self.notes = notes
        self.session = session
        self.instructor = instructor
        self.email = email
        self.occupied = int(occupied)
        self.capacity = int(capacity)
        self.time = []
        self.closed = Section.check_closed(occupied, capacity)

    def add_a_course_time(self, course_time):
        self.time.append(course_time)
