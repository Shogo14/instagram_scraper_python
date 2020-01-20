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
    webpageLink = urlopen(url).read()
    soup = BeautifulSoup(webpageLink, 'html.parser')
    videourl = soup.find("meta",  property="og:video")
    if videourl == None:
        video_link = original
    else:
        video_link = videourl["content"]
    return video_link

def insert_posts(db_con,post_id,data_name2,caption,user_id,posted_date):
    cur = db_con.cursor()

    sql = "INSERT INTO posts (post_id, data_name2, caption, user_id, posted_date) VALUES (%s, %s, %s, %s, %s)"
    val = (post_id,data_name2,caption,user_id,posted_date)
    cur.execute('SET NAMES utf8mb4')
    cur.execute("SET CHARACTER SET utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute(sql,val)
    db_con.commit()

    cur.close
    db_con.close

def insert_post_media(db_con,post_id,media_type,src):
    cur = db_con.cursor()

    sql = "INSERT INTO post_media (post_id,media_type,src) VALUES (%s, %s, %s)"
    val = (post_id,media_type,src)
    cur.execute(sql,val)
    db_con.commit()

    cur.close
    db_con.close

def exist_post(db_con,post_id):
    cur = db_con.cursor()

    sql = "SELECT count(*) FROM posts WHERE post_id = %s"
    condition = (post_id,)
    
    cur.execute(sql,condition)
    result = cur.fetchone()

    cur.close
    db_con.close
    if result[0] > 0:
        return True
    else:
        return False

instagram = Instagram()
cur = db_con.cursor()
sql = "SELECT profinfo13 ,name2 FROM data WHERE profinfo13 != '' ORDER BY name2 ASC"
cur.execute(sql)
rows = cur.fetchall()
cur.close
db_con.close

for i in range(100):
    print('----------Start!-------------')
    user_id = rows[i][0]
    data_name2 = rows[i][1]
    accounts = instagram.search_accounts_by_username(user_id)
    medias = []
    try:
        medias = instagram.get_medias(user_id, 25)
    except Exception as e:
        print(str(user_id) + "：削除されてる可能性があります。:"+str(e))

    if len(accounts) > 0:
        if len(medias) > 0:
            media = medias[0]
            print(media)
            caption = media.caption
            post_id = media.identifier
            exist_flg = exist_post(db_con,post_id)
            if not exist_flg:
                posted_date = datetime.fromtimestamp(media.created_time) 
                media_type = media.type
                post_media_src = ''
                if media_type == 'video':
                    # 動画URL
                    post_media_src = video_r(media.link, media.image_high_resolution_url)
                elif media_type == 'sidecar':
                    sc_medias = instagram.get_media_by_url('https://www.instagram.com/p/' + media.short_code).sidecar_medias
                    for sc_media in sc_medias:
                        sc_media_type = sc_media[0]
                        post_media_src = sc_media[1]
                        if sc_media_type == 'GraphVideo':
                            media_type = 'video'
                            print('this is GraphVideo')
                        elif sc_media_type == 'GraphImage':
                            media_type = 'image'
                            print('this is Graphimage')
                        else:
                            print('othre???')
                else:
                    # 画像URL
                    print(media.image_high_resolution_url)

                insert_posts(db_con,post_id,data_name2,caption,user_id,posted_date)
                insert_post_media(db_con,post_id,media_type,post_media_src)
            else:
                print('exist! not insert')

        else:
            print('投稿なし')
    else:
        print('アカウントなし')
