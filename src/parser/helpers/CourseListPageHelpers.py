from bs4 import BeautifulSoup


def make_soup(page_text, features='html.parser'):
    return BeautifulSoup(page_text, features=features)


def get_max_page(page_soup) -> int:
    pagination_list = page_soup.select('.ui.pagination.menu a:not(.icon)')
    list_page_anker = pagination_list[-1]
    max_page = int(list_page_anker.text)
    return max_page


def get_tbody(page_soup) -> object:
    return page_soup.find('tbody')


def get_rows(tbody) -> list[object]:
    return tbody.find_all('tr')


def get_cols(row) -> list[object]:
    return row.find_all('td')
