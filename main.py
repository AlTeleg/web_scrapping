from bs4 import BeautifulSoup
import requests
from pprint import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'
HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639'
              '149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b46710'
              '3cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKi'
                  't/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'
}


def light_search(keywords):
    article_list = []
    art_text_list = []
    indication = False
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, features='html.parser')
    articles = soup.find_all("article")
    for article in articles:
        spans = article.find('h2').find_all('span')
        try:
            texts = article.find('div', class_="article-formatted-body "
                                               "article-formatted-body article-formatted-body_version-2").find_all('p')
        except:
            texts = []
        hubs = article.find('div', class_="tm-article-snippet__hubs").find('span').find('a').find_all('span')
        art_text_list.append(','.join([i.text for i in spans] + [i.text for i in texts] + [i.text for i in hubs]))
        for word in keywords:
            if word.lower() in ' '.join([str(x).lower() for x in art_text_list]):
                indication = True
        if indication:
            article_list.append([f'Дата - {article.find("time").attrs["datetime"][:10]}',
                                 f'Заголовок - "{article.find("h2").find("span").text}"',
                                 f'Ссылка - https://habr.com'
                                 f'{article.find(class_="tm-article-snippet__title-link").attrs["href"]}'])
        art_text_list = []
        indication = False
    pprint(article_list)


def deep_search(keywords):
    article_list = []
    art_text_list = []
    link_list = []
    indication = False
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, features='html.parser')
    article_list_tmp = soup.find_all(class_="tm-article-snippet__title-link")
    for article in article_list_tmp:
        a = article.get('href')
        link_list.append(a)
    for link in link_list:
        res = requests.get('https://habr.com' + link, headers=HEADERS)
        soup = BeautifulSoup(res.text, features='html.parser')
        a = soup.find('article')
        texts = a.find_all('p')
        spans = a.find_all('span')
        art_text_list.append(','.join([i.text for i in spans] + [i.text for i in texts]))
        for word in keywords:
            if word.lower() in ' '.join([str(x).lower() for x in art_text_list]):
                indication = True
        if indication:
            article_list.append([f'Дата - {a.find("time").attrs["datetime"][:10]}',
                                 f'Заголовок - "{a.find_all("span")[3].text}"',
                                 f'Ссылка - https://habr.com'
                                 f'{link}'])
        art_text_list = []
        indication = False
    pprint(article_list)


if __name__ == '__main__':
    # light_search(KEYWORDS)
    deep_search(KEYWORDS)
