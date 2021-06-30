import requests
import time
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as BS
import time
import xlwt
import xlrd


def parse_categ():
    name_categories = []
    name_subcategories = []
    r = requests.get('https://mosopttorg.com/', verify=False)
    html = BS(r.content, 'html.parser')
    for el in html.select('div.cat-title'):
        name = el.text
        name_categories.append(name)
    for el in html.select('div.cat-title a'):
        name = el.attrs['href']
        print(f'Переходим по ссылке {name}')
        r1 = requests.get(name, verify=False)
        html1 = BS(r.content, 'html.parser')
        for el in html1.select('div.cat-title'):
            name = el.text
            name_categories.append(name)

