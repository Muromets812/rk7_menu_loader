import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import re
import pandas as pd

BASIC = HTTPBasicAuth('HTTPUSER', '9011')
HEADER = {'X-Requested-With': 'XMLHttpRequest', }
REG_PRICE = r'ObjectID="(\d*)"\sValue="(\d*)"'
REG_MENU = r'Item\sIdent="(\d*)"\sName="([а-яА-Я-\s\w,.\/]*)"'
menu = []
price = []


def get_data(xml_file):
    with open(xml_file, 'r') as f:
        r_data = f.read()
        response = requests.get('https://127.0.0.1:2323/rk7api/v0/xmlinterface.xml', auth=BASIC, headers=HEADER,
                                data=r_data, verify=False)
        soup = BeautifulSoup(response.text, features='xml')
        data = re.split(r"\n", str(soup.find_all('Items')))
    return data


if __name__ == "__main__":
    for item in get_data('prices.xml'):
        try:
            data_filter = re.search(REG_PRICE, item)
            price.append({'ID': data_filter.group(1), 'PRICE': data_filter.group(2)})
        except AttributeError:
            continue

    for item in get_data('menu.xml'):
        try:
            data_filter = re.search(REG_MENU, item)
            menu.append({'ID': data_filter.group(1), 'NAME': data_filter.group(2)})
        except AttributeError:
            continue

    result = pd.DataFrame(menu).merge(pd.DataFrame(price), on='ID')
    result.to_excel('RK7_MENU.xlsx', sheet_name='Menu', index=False)
