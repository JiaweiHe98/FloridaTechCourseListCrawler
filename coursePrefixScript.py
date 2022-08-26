from typing_extensions import Self
from bs4 import BeautifulSoup
import json
import re

alert_pattern = re.compile(r'\((.+)\)')
class_pattern = re.compile(r'\w+')


class ColorPalette():

    def __init__(self) -> None:
        self.colors = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33",
                       "#D9CE53", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]

        self.pt = 0
        self.length = len(self.colors)

    def getNext(self):
        if (self.pt >= self.length):
            self.pt = 0

        color = self.colors[self.pt]
        self.pt += 1
        return color


def parse():
    prefix_class = {}

    color_palette = ColorPalette()

    with open('./coursePrefix.html', 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, features='html.parser')
    all_tbody = soup.find_all('tbody')
    all_tr = []

    for tbody in all_tbody:
        all_tr += tbody.find_all('tr')

    for tr in all_tr:
        tds = tr.find_all('td')

        if len(tds) != 2:
            continue

        prefix = tds[0].text.strip()

        strip_res = tds[1].text.strip()

        if res := alert_pattern.search(strip_res):
            alert = res[1]
        else:
            alert = None

        res = class_pattern.match(strip_res)

        class_name = res[0]

        prefix_class[prefix] = {'class': class_name,
                                'alert': alert}

    # with open('coursePrefix.json', 'w') as f:
    #     json.dump(prefix_class, f)

    with open('./courseList.json') as f:
        courseList = json.load(f)

    all_prefix = {}

    for semester in ['fall', 'spring', 'summer']:

        for prefix in courseList[semester]:

            if prefix in prefix_class:

                all_prefix[prefix] = {'class': prefix_class[prefix]['class'],
                                      'alert': prefix_class[prefix]['alert'],
                                      'color': color_palette.getNext()}

            else:
                all_prefix[prefix] = {'class': f'({prefix})',
                                      'alert': None,
                                      'color': color_palette.getNext()}

    with open('./coursePrefix.json', 'w') as f:
        json.dump(all_prefix, f)


if __name__ == '__main__':
    parse()
