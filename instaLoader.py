from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

L = instaloader.Instaloader(download_pictures=True, download_videos=False, download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False, post_metadata_txt_pattern="")

posts = L.get_hashtag_posts('urbanphotography')
# or
# posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()

SINCE = datetime(2018, 5, 1)
UNTIL = datetime(2018, 5, 2)

for post in L.get_hashtag_posts('mclarenf1'):
    L.download_post(post, target='#mclarenf1')