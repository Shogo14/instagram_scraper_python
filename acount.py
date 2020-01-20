from igramscraper.instagram import Instagram
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import MySQLdb





instagram = Instagram()
# instagram.set_proxies(proxies)
# カーソルを取得する
medias = []
accounts = instagram.search_accounts_by_username('rio.0720')

medias = instagram.get_medias('rio.0720', 25)


if len(medias) > 0:
    print('アカウント存在する')
else:
    print('アカウント存在しない')
