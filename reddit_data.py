import praw
import config
from pprint import pprint
import sys
import spotipy
import spotipy.util as util
import time

sp = None
spotify_token = None
reddit_client = None
current_time = None
end_time = None
SECONDS_PER_DAY = 86400

subreddit_to_flair = {u'edm': u'New'}

def setup():
	global sp, spotify_token, reddit_client, end_time

	spotify_scope = 'playlist-modify-public user-library-read'
	spotify_username = config.spotify_profile_uri
	spotify_token = util.prompt_for_user_token(spotify_username, scope=spotify_scope, client_id=config.spotipy_client_id, client_secret=config.spotipy_client_secret, redirect_uri=config.spotipy_redirect_uri)
	if spotify_token:
		sp = spotipy.Spotify(auth=spotify_token)

	reddit_client = praw.Reddit(user_agent='MySimpleBot v0.1', redirect_uri='http://localhost:1090', client_id=config.client_id, client_secret=config.client_secret,
							username=config.username, password=config.password)

	end_time = time.time() - SECONDS_PER_DAY

setup()

def pull_reddit_tracks():
	track_ids = set()

	for sub in subreddit_to_flair.iterkeys():
		subreddit = reddit_client.subreddit(sub)
		new_submissions = subreddit.new()

		while True:
			submission = new_submissions.next()
			if submission.created_utc < end_time:
				break
			elif submission.link_flair_text != subreddit_to_flair[sub]:
				continue

			if 'album' in submission.url:
				music_id = submission.url.rsplit('/', 1)[1]
				album = sp.album(music_id)
				track_ids = []
		for track in album['tracks']['items']:
			track_ids.append(track['id'])



subreddit = reddit_client.subreddit('edm')

new_submissions = subreddit.new()
i = 0
while True:
	submission = new_submissions.next()
	i += 1

	# check that time is within 24 hours
	# breaks once already seen all the new posts
	if i > 20:
		break
	elif submission.link_flair_text != u'New':
		continue

	if 'album' in submission.url:
		print 'PRINTING ALBUM'
		music_id = submission.url.rsplit('/', 1)[1]
		if '?' in music_id:
			music_id = music_id[:music_id.index('?')]
		album = sp.album(music_id)
		track_ids = []
		for track in album['tracks']['items']:
			track_ids.append(track['id'])
		result = sp.user_playlist_add_tracks(config.spotify_profile_id, config.spotify_playlist_uri, track_ids)
		print result
	elif 'track' in submission.url:
		print "PRINTING TRACK"
		print submission.url
		track_id = submission.url.rsplit('/', 1)[1]
		if '?' in track_id:
			track_id = track_id[:track_id.index('?')]
		track_id = [track_id]
		print track_id
		# tracks_uri = 'spotify:track:'+music_id
		result = sp.user_playlist_add_tracks(config.spotify_profile_id, config.spotify_playlist_uri, track_id)
		print result


	# music_id = submission.url.rsplit('/', 1)[1]
	# print submission.url
	# print music_id
	# if spotify_token:
	# 	results = sp.user_playlist_add_tracks(config.spotify_profile_id, config.spotify_playlist_uri, music_id)
 #    	print results
	# pprint(vars(submission))

# for submission in subreddit.new():
# 	pprint(vars(submission))

# 	print "-------------------------------------"
# 	print(submission.link_flair_text == u'Upcoming')
# 	i += 1
# 	if i >= 1:
# 		sys.exit()

#  'domain': u'open.spotify.com',
#  'link_flair_text': u'New',
#'url': u'https://open.spotify.com/album/1m3mf7xkXIwssVriaaTjOS',

# 'media': {u'oembed': {u'description': u'AV\u012aCI (01), an album by Avicii on Spotify',
 #                       u'height': 380,
 #                       u'html': u'<iframe class="embedly-embed" src="//cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fopen.spotify.com%2Fembed%2Falbum%2F1m3mf7xkXIwssVriaaTjOS&url=https%3A%2F%2Fopen.spotify.com%2Falbum%2F1m3mf7xkXIwssVriaaTjOS&image=https%3A%2F%2Fi.scdn.co%2Fimage%2F23f34e014681b5866454e7e8d55f9f349169e92e&key=522baf40bd3911e08d854040d3dc5c07&type=text%2Fhtml&schema=spotify" width="300" height="380" scrolling="no" frameborder="0" allowfullscreen></iframe>',
 #                       u'provider_name': u'Spotify',
 #                       u'provider_url': u'https://www.spotify.com',
 #                       u'thumbnail_height': 640,
 #                       u'thumbnail_url': u'https://i.scdn.co/image/23f34e014681b5866454e7e8d55f9f349169e92e',
 #                       u'thumbnail_width': 640,
 #                       u'title': u'AV\u012aCI (01)',
 #                       u'type': u'rich',
 #                       u'version': u'1.0',
 #                       u'width': 300},
 #           u'type': u'open.spotify.com'},
 # 'media_embed': {u'content': u'<iframe class="embedly-embed" src="//cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fopen.spotify.com%2Fembed%2Falbum%2F1m3mf7xkXIwssVriaaTjOS&url=https%3A%2F%2Fopen.spotify.com%2Falbum%2F1m3mf7xkXIwssVriaaTjOS&image=https%3A%2F%2Fi.scdn.co%2Fimage%2F23f34e014681b5866454e7e8d55f9f349169e92e&key=522baf40bd3911e08d854040d3dc5c07&type=text%2Fhtml&schema=spotify" width="300" height="380" scrolling="no" frameborder="0" allowfullscreen></iframe>',
 #                 u'height': 380,
 #                 u'scrolling': False,
 #                 u'width': 300},