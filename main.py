from threading import Thread
from urllib import request, parse
import json

Words = []

def main():
    global Words

    keywords = open('keywords.txt', 'r').read().split('\n')

    for keyword in keywords:
        get_pages(keyword)

        res = []

        for word in Words:
            if word not in res:
                res.append(word)

        res.sort()

        Words = []
        f = open(f'result/{keyword}.txt', 'w')

        f.write('\r\n'.join(res))

def get_pages(keyword):
    print(f'{keyword} 파싱중...')

    keyword += '??'
    threads = []
    last_page = get_last_page(keyword)

    for page in range(1, last_page + 1):
        url = get_url(keyword, page)
        th = Thread(target=get_words, args=(url,))

        th.start()
        threads.append(th)

    for th in threads:
        th.join()

def get_words(url):
    req = request.Request(url)
    r = request.urlopen(req).read()
    data = json.loads(r.decode('utf-8'))

    for item in data['searchResultMap']['searchResultListMap']['WORD']['items']:
        Words.append(item['handleEntry'])

def get_url(keyword, page):
    return f'https://ko.dict.naver.com/api3/koko/search?query={parse.quote(keyword)}&range=word&page={page}'

def get_last_page(keyword):
    req = request.Request(get_url(keyword, 1))
    r = request.urlopen(req).read()
    data = json.loads(r.decode('utf-8'))

    return data['pagerInfo']['totalPages']

if __name__ == '__main__':
    main()
