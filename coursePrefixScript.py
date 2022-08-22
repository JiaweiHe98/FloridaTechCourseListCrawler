from bs4 import BeautifulSoup
import json
import re

alert_pattern = re.compile(r'\((.+)\)')
class_pattern = re.compile(r'\w+')


def parse():
    prefix_class = {}

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

        prefix_class[prefix] = {'class': class_name, 'alert': alert}

    with open('coursePrefix.json', 'w') as f:
        json.dump(prefix_class, f)


if __name__ == '__main__':
    parse()
