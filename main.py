from igramscraper.instagram import Instagram

instagram = Instagram()

medias = instagram.get_medias("sweet.teabby", 1)

# これはtop1の最近写真
print(medias)

# 一番最近の写真を取ってきます
media = medias[0]

print(media)

# side car mediaを取得する
media = instagram.get_media_by_url('https://www.instagram.com/p/' + media.short_code)

print(media.sidecar_medias)
