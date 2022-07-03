import requests
from bs4 import BeautifulSoup
import lxml
import csv
URL ='https://auto.ria.com/newauto/marka-toyota/'
HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept':'*/*'
}
HOST ='https://auto.ria.com'


def get_html(url,params=None):
    req = requests.get(url=url,headers=HEADERS,params=params)
    return req


def get_pages(html):
    pg = BeautifulSoup(html,'lxml')
    try:
        pg.find('nav', {'class': 'unstyle pager'}).find_all('span', {'class': 'page-item mhide'})
    except Exception:
        page = '1'
    else:
        page = pg.find('nav',{'class':'unstyle pager'}).find_all('span',{'class':'page-item mhide'})[-1].text

    return page

def get_content(html):
    soup = BeautifulSoup(html,'lxml')
    items = soup.find_all('a',{'class':'proposition_link'})
    cars = []
    for data in items:
        uah_price = data.find('div',{'class': 'proposition_price'}).find('span',{'class':'size16'})
        if uah_price:
            uah_price = uah_price.text.strip()
        else:
            uah_price = 'price nope'
        cars.append(
            {
                'title': data.find('div',{'class':'proposition_equip'}).text.strip(),
                'link': HOST+data.get('href'),
                'usd_price': data.find('div',{'class':'proposition_price'}).find('span').text.strip(),
                'grn_price': uah_price,
                'place': data.find('div',{'class':'proposition_information'}).find_all('span')[0].text.strip()
            }
        )
    return cars


def save_file(items):
    with open('cars.csv','w',encoding='utf-8',newline='') as csvfile:
        fieldnames = ['title','link','usd_price','grn_price','place']
        writer = csv.DictWriter(csvfile,delimiter=';',fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
       page_count = get_pages(html.text)
       cars = []
       for page in range(1,int(page_count)+1):
            print(f"парсинн страницы {page} из {page_count} ....")
            html = get_html(URL,params=f'page={page}')
            cars.extend(get_content(html.text))
       save_file(cars)
       print(len(cars))
    else:
     print(f"error {html.status_code}")



parse()



