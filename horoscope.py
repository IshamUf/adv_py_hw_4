import requests
from bs4 import BeautifulSoup


def get_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.find('div', class_='article__item article__item_alignment_left article__item_html').get_text(
            strip=True)
        return text
    except Exception as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None


def get_horoscope(sign=None):
    if sign is None:
        return get_text(f"https://horo.mail.ru/")
    else:
        return get_text(f"https://horo.mail.ru/prediction/{sign}/today/")


print(get_horoscope('dfgvdf'))
print(str(None))