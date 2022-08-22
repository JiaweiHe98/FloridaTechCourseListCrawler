# from ..model import Entry
#
#
# class EntryBuilder:
#
#     crn: int
#     prefix: str
#     suffix: int
#     section: str
#     cr: tuple[int, int]
#     title: str
#     info: str
#     notes: str
#     days: str
#     times: tuple[tuple[int, int], tuple[int, int]]
#     place: str
#     instructor: str
#     email: str
#     occupied: int
#     capacity: int
#
#     def __int__(self):
#         self.initialized = [False] * 15
#
#     def set_crn(self, crn):
#         self.crn = crn
#         self.initialized[0] = True
#         return self
#
#     def set_prefix(self, prefix):
#         self.prefix = prefix
#         self.initialized[1] = True
#         return self
#
#     def set_suffix(self, suffix):
#         self.suffix = suffix
#         self.initialized[2] = True
#         return self
#
#     def set_section(self, section):
#         self.section = section
#         self.initialized[3] = True
#         return self
#
#     def set_cr(self, cr):
#         self.cr = cr
#         self.initialized[4] = True
#         return self
#
#     def set_title(self, title):
#         self.title = title
#         self.initialized[5] = True
#         return self
#
#     def set_info(self, info):
#         self.info = info
#         self.initialized[6] = True
#         return self
#
#     def set_notes(self, notes):
#         self.notes = notes
#         self.initialized[7] = True
#         return self
#
#     def set_days(self, days):
#         self.days = days
#         self.initialized[8] = True
#         return self
#
#     def set_times(self, times):
#         self.times = times
#         self.initialized[9] = True
#         return self
#
#     def set_place(self, place):
#         self.place = place
#         self.initialized[10] = True
#         return self
#
#     def set_instructor(self, instructor):
#         self.instructor = instructor
#         self.initialized[11] = True
#         return self
#
#     def set_email(self, email):
#         self.email = email
#         self.initialized[12] = True
#         return self
#
#     def set_occupied(self, occupied):
#         self.occupied = occupied
#         self.initialized[13] = True
#         return self
#
#     def set_capacity(self, capacity):
#         self.capacity = capacity
#         self.initialized[14] = True
#         return self
#
#     def build(self):
#         for isInitialized in self.initialized:
#             if not isInitialized:
#                 raise Exception('Entry instance not properly initialized!')
#
#         return Entry.from_builder(self)
#
#
