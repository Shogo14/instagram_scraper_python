# -*- coding: utf-8 -*-
from igramscraper.instagram import Instagram
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import MySQLdb

# 接続する
db_con = MySQLdb.connect(
user='root',
passwd='fallout14',
host='localhost',
db='db_cast_crawler',
charset='utf8'
)


def video_r(url, original):
    video_link = ""
    webpageLink = urlopen(url+'/?hl=ja').read()
    soup = BeautifulSoup(webpageLink, 'html.parser')
    videourl = soup.find("meta",  property="og:video")
    if videourl == None:
        print('none')
        video_link = original
    else:
        video_link = videourl["content"]
    return video_link


instagram = Instagram()
# cur = db_con.cursor()
# sql = "SELECT profinfo13 ,name2 FROM data WHERE profinfo13 != '' ORDER BY name2 ASC"
# cur.execute(sql)
# rows = cur.fetchall()
# cur.close
# db_con.close

# for row in rows:
print('----------Start!-------------')
user_id = 'mio_nyx'
# data_name2 = row[1]
accounts = instagram.search_accounts_by_username(user_id)
medias = []
try:
    medias = instagram.get_medias(user_id, 25)
except Exception as e:
    print(str(user_id) + "：削除されてる可能性があります。:"+str(e))

if len(accounts) > 0:
    if len(medias) > 0:
        media = medias[4]
        caption = media.caption
        post_id = media.identifier
        posted_date = datetime.fromtimestamp(media.created_time) 
        media_type = media.type
        post_media_src = ''
        if media_type == 'video':
            # 動画URL
            post_media_src = video_r(media.link, media.image_high_resolution_url)
        elif media_type == 'sidecar':
            print(user_id)
            print(media.link)
            print(media.image_high_resolution_url)
            post_media_srcs = video_r(media.link, media.image_high_resolution_url)
            print('koko: '+post_media_srcs)
            # sc_medias = instagram.get_media_by_url('https://www.instagram.com/p/' + media.short_code).sidecar_medias
            # for sc_media in sc_medias:
            #     sc_media_type = sc_media[0]
            #     post_media_src = sc_media[1]
            #     if sc_media_type == 'GraphVideo':
            #         media_type = 'video'
            #         print('this is GraphVideo')
            #     elif sc_media_type == 'GraphImage':
            #         media_type = 'image'
            #         print('this is Graphimage')
            #     else:
            #         print('othre???')
        else:
            # 画像URL
            print(media.image_high_resolution_url)


    else:
        print('投稿なし')
else:
    print('アカウントなし')
