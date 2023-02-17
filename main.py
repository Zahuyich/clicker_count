import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(url, token):
    headers = {
      'Authorization': f'Bearer {token}'
    }
    long_url = {"long_url": url}
    response = requests.post(
      'https://api-ssl.bitly.com/v4/shorten',
      headers=headers, 
      json=long_url
    )
    response.raise_for_status()
    short_link = response.json()
    return short_link['id']


def count_clicks(url, token):
    parsed_link = urlparse(url)
    short_link= f"{parsed_link.netloc}{parsed_link.path}"
  
    headers = {"Authorization": token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, token):
    parsed_link = urlparse(url)
    short_link= f"{parsed_link.netloc}{parsed_link.path}"
  
    headers = {"Authorization": token}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv('.env')
    api_key = os.environ['BITLY_TOKEN']
    url = input('Введите ссылку:')

    try:
        if is_bitlink(url, api_key):
            print('Clicks_count: ', count_clicks(url, api_key))
        else:
            print('Bitlink: ', shorten_link(url, api_key))
    except requests.exceptions.HTTPError as e:
            print('Error: ', e)


if __name__ == '__main__':
    main()
  
