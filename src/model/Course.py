class Course:
    sections: dict
    # title: str
    # cr: list[float, float]

    def __init__(self) -> None:
        # self.title = title
        # self.cr = cr
        self.sections = {}

    def add_a_section(self, section_name: str, section: object) -> None:
        if section_name in self.sections:
            raise Exception(
                f'Section name collision! section_name: {section_name}' +
                f' exist: {str(self.sections[section_name])} new: {str(section)}')

        self.sections[section_name] = section
