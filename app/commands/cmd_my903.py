import json
import requests

def my903(update, context):
    r = requests.post('https://my903.com/903openbox/api/post', data={'page': 0, 'profile_id': '903songtable1', 'post_type': 0})
    posts = json.loads(r.content)['data']['posts']
    photo_url = 'https://my903.com/903openbox' + posts[0]['thumbnail_image_url']
    caption = posts[0]['post_title'] + '\n'
    for index, song in enumerate(posts[0]['post_content'].split('<br />')):
        if index > 9:
            break
        else:
            caption += song.replace('<p>', '') + '\n'
    context.bot.send_photo(chat_id=update.message.chat.id, photo=photo_url, caption=caption)
