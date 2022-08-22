import requests
import urllib3
import asyncio


def get_html(full_url, headers=None, verify=False):
    if not verify:
        urllib3.disable_warnings()

    res = requests.get(url=full_url, headers=headers, verify=verify)
    return res.text


async def get_html_async(session, full_url, headers=None, verify=False):
    async with session.get(full_url) as res:
        res_text = await res.text()
    return res_text


def save_page(semester, page_num, page_text):
    with open(f'src/html/{semester}_{page_num}.html', 'w') as f:
        f.write(page_text)
