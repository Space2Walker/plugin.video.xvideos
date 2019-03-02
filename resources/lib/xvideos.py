# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcplugin
import resources.lib.helper as helper

#################################
#			get_cats			#
#################################
'''
crawls the Catergorys from xvideos.com
and returns them as a list of dicts

[{'category': 'Pornos auf Deutsch', 'link': 'https://xvideos.com/lang/deutsch'}, 
 {'category': '3d', 'link': 'https://xvideos.com/?k=3d&top'}]
'''
def get_cats():
	url = 'https://xvideos.com/'
	cats = []
	soup = helper.get_soup(url)
	divs = soup.find(id="main-cat-sub-list")

	for div in divs.find_all('a', href=True): 
		cats.append(
			dict([
				('category', div.text.lstrip(' ')),
				('link', url[:-1] + div.get('href'))
			]))

	return cats

#################################
#			get_vids			#
#################################
'''
crawls a given url form xvideos.com for videos
and returns them as a list of dicts
if a catergory is given it will be added to the dict

a returnd dict looks like this
	 KEYS	 VALUE 
[{ 'title': 'BF HAVE 8 INC BUT YOUR ', 
    'link': 'https://xvideos.com/video45543479/nasty_girl_masturbate',
'duration': '5 min', 
   'thumb': 'https://img-hw.xvideos-cdn.com/videos/thumbs169/a3/ed/36/a3ed367bcb5b699a6cf8eaa80a70a9ad/a3ed367bcb5b699a6cf8eff80a69a9ad.14.jpg', 
     'res': '720p', 
   'views': '13k',
'uploader': 'hans',
'category': 'Grany'}]
'''
def get_vids(url, category='none'):

	hardcoded = 'https://xvideos.com'
	video_info = []
	videos = [] 
	soup = helper.get_soup(url)

	#####################
	# get the video div and make a dict from both divs inside

	video_div = soup.find_all("div", class_="thumb-block")

	for video in video_div: 
	
		videos.append( 
			dict([('under', video.find("div", class_="thumb-under")),
				('inside', video.find("div", class_="thumb-inside"))
				]))

	############################################
	# get the infos from the dict and make the final info dict

	for info in videos:
    
		inside = info['inside']
		under = info['under']

		title = under.find("a", href=True)
		duration = helper.convert_duration(under.find("span", class_="duration").text)
		views = under.find("span", class_="sprfluous").nextSibling

		
		try:
			uploader = under.find("span", class_="name").text
		except AttributeError:
			views = under.find("span", class_="duration").nextSibling
			uploader = "Unknown"
	
		img = inside.find("div", class_="thumb").find('img')
		res_tag = inside.find(class_="video-hd-mark")

		try:
			res = res_tag.text
		except AttributeError:
			res = ''

		video_info.append(
			dict([
				('title', title.get('title')),
				('link', hardcoded + title.get('href')),
				('duration', duration),
				('thumb', img.get('data-src')),
				('res', res),
				('views', views[1:]),
				('uploader', uploader),
				('category', category)
				]))
	return video_info


def play_video(_handle, video):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    soup = helper.get_soup(video)
    
    div = soup.find("div", id="video-player-bg")            #find div
    script_tag = div.find_all("script")[4]                  #find script tag in div
    
    tmp = script_tag.string.split("setVideoHLS('")[-1]      #cleanup request
    m3u_link = tmp.split("')", 1)[0]


    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=m3u_link)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

