import requests
from typing import List
from bs4 import BeautifulSoup


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'upgrade-insecure-requests': '1'
}


def get_number_of_deals(text: str, region: str) -> int:
  response = requests.get(f'https://www.avito.ru/{region}',
                          params={'q': text},
                          headers=headers)

  soup = BeautifulSoup(response.text, 'lxml')
  number_of_deals = soup.find('span', class_='page-title-count-1oJOc').text
  return int(number_of_deals.replace(' ', ''))


def get_top5_deals(text: str, region: str) -> List[str]:
  avito_url = 'https://www.avito.ru'
  response = requests.get(f'{avito_url}/{region}',
                          params={'q': text},
                          headers=headers)

  soup = BeautifulSoup(response.text, 'lxml')
  deals = soup.find_all('div', class_='iva-item-titleStep-2bjuh')[:5]
  deals_urns = [deal.a['href'] for deal in deals]
  full_links = [avito_url + urn for urn in deals_urns]
  return full_links
