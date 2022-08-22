# class Entry:
#     crn: str
#     prefix: str
#     suffix: int
#     section: str
#     cr: tuple[int]
#     title: str
#     info: str
#     notes: str
#     days: str
#     times: tuple[tuple[int]]
#     place: str
#     instructor: str
#     email: str
#     occupied: int
#     capacity: int
#
#     @classmethod
#     def from_builder(cls, entry_builder):
#         eb = entry_builder
#         cls(
#             eb.crn,
#             eb.prefix,
#             eb.suffix,
#             eb.section,
#             eb.cr,
#             eb.title,
#             eb.info,
#             eb.notes,
#             eb.days,
#             eb.times,
#             eb.place,
#             eb.instructor,
#             eb.email,
#             eb.occupied,
#             eb.capacity
#         )
#
#
# if __name__ == '__main__':
#     Entry.from_builder(None)
#
#
