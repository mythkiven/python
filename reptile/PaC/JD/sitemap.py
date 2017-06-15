



# 获取整个站点的所有 url网址
import requests
from bs4 import BeautifulSoup
import re

urlll = 'http://www.cnblogs.com'
urlllsss =[]
def get_all_url(url):
    urls = []
    web = requests.get(url)
    soup = BeautifulSoup(web.text)
    # 通过正则过滤合理的url(针对与cnblogs.com来讲)
    tags_a = soup.findAll(name='a', attrs={'href': re.compile("^https?://")})
    try:
        for tag_a in tags_a:
            urls.append(tag_a['href'])
            # return urls
    except:
        pass
    return urls


# 得到所有freebuf.com下的url
def get_local_urls(url):
    local_urls = []
    urls = get_all_url(url)
    for _url in urls:
        ret = _url
        if urlll in ret.replace('//', '').split('/')[0]:
            local_urls.append(_url)
    return local_urls


# 得到所有的不是freebuf.com域名的url
def get_remote_urls(url):
    remote_urls = []
    urls = get_all_url(url)
    for _url in urls:
        ret = _url
        if urlll not in ret.replace('//', '').split('/')[0]:
            remote_urls.append(_url)
    return remote_urls


def __main__():
    url = urlll
    rurls = get_remote_urls(url)
    urlllsss =  rurls
    print("--------------------remote urls-----------------------")
    for ret in rurls:
        print('1')
        urlllsss.extend(get_remote_urls(url))
        print('2')


    print("---------------------localurls-----------------------")
    lurls = get_local_urls(url)
    for ret in lurls:
        urlllsss.extend(get_remote_urls(url))

    print("---------------------------------------")
    for ret in urlllsss:
        print(ret)


if __name__ == '__main__':
    __main__()