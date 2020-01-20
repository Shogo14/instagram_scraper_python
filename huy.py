from igramscraper.instagram import Instagram
from bs4 import BeautifulSoup
from urllib.request import urlopen

# インスタから取得できるデータは写真（複数なら2枚目以降も）、動画、投稿のID、ユーザーのID、投稿時間、この辺は問題なく取得できますか？
def video_r(url, original):
    video_link = ""
    webpageLink = urlopen(url).read()
    soup = BeautifulSoup(webpageLink, 'html.parser')
    videourl = soup.find("meta",  property="og:video")
    if videourl == None:
        print('none')
        video_link = original
    else:
        print('else')
        video_link = videourl["content"]
    return video_link

def sidecar_r(url, original):
    video_link = ""
    webpageLink = urlopen(url).read()
    soup = BeautifulSoup(webpageLink, 'html.parser')
    images = soup.find_all('image', class_='FFVAD')
    if images == None:
        video_link = original
    else:
        video_link = images["src"]
    return video_link

instagram = Instagram()

medias = instagram.get_medias("mio_nyx", 25)

# これはtop２５の最近写真
# print(medias)

# 一番最近の写真を取ってきます
media = medias[4]

print(media)
print(media.caption)


if media.type == 'video':
    # 動画URL
    print(video_r(media.link, media.image_high_resolution_url))
elif media.type == 'sidecar':
    media = instagram.get_media_by_url('https://www.instagram.com/p/' + media.short_code)
    sidecarmedias = media.sidecar_medias
    print(sidecarmedias)
    for sidecar in sidecarmedias:
        print('url: '+sidecar)
else:
    # 画像URL
    print(media.image_high_resolution_url)
