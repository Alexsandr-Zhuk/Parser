import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cars.csv'
host = 'https://cars.av.by'
url = 'https://cars.av.by/audi/a6'
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    r = requests.get(url, headers=headers, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')
    cars = []

    for item in items:
        cars.append(
            {
                'title': item.find('h3', class_='listing-item__title').get_text(strip=True),
                'link_car': host + item.find('h3', class_='listing-item__title').find('a').get('href'),
                'price': item.find('div', class_='listing-item__price').get_text(strip=True),
                'options': item.find('div', class_='listing-item__params').get_text(strip=True),
            }
        )
    return cars


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Название авто', 'Ссылка', 'Цена', 'Характеристика'])
        for item in items:
            writer.writerow([item['title'], item['link_car'], item['price'], item['options']])


def parser():
    pages = input('Укажите количество станиц:')
    pages = int(pages)
    html = get_html(url)
    if html.status_code == 200:
        cars = []
        for pages in range(1, pages):
            print(f'Парсим страницу: {pages}')
            html = get_html(url, params={'page': pages})
            cars.extend(get_content(html.text))
            save_doc(cars, CSV)
        pass
    else:
        print('Error')


parser()
