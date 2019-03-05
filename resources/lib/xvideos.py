# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcplugin
import resources.lib.helper as helper


def get_vids(url, category='none'):
    '''crawls a given url form xvideos.com for videos
    and returns them as a list of dicts
    if a catergory is given it will be added to the dict
    '''
    hardcoded = 'https://xvideos.com'
    video_info = []
    videos = []
    soup = helper.get_soup(url)
    videos = soup.find_all("div", class_="thumb-block")
    page_lis = soup.find("div", class_="pagination").find_all('li')

    if page_lis[-1].a.text == "Next":
        page = page_lis[-2].a.text
    else:
        page = page_lis[-1].a.text

    for info in videos:
        inside = info.find("div", class_="thumb-inside")
        under = info.find("div", class_="thumb-under")
        title = under.find("a", href=True)
        img = inside.find("div", class_="thumb").find('img')
        res_tag = inside.find(class_="video-hd-mark")
        views = under.find("span", class_="sprfluous").nextSibling
        duration = helper.convert_duration(
            under.find("span", class_="duration").text)

        # sometimes there is no uploader
        try:
            uploader = under.find("span", class_="name").text
        except AttributeError:
            # Is no Uploader there, the views are difrent also
            views = under.find("span", class_="duration").nextSibling
            uploader = "Unknown"

        # sometimes there is no resolution tag
        try:
            res = res_tag.text
        except AttributeError:
            res = None

        video_info.append(
            dict([
                ('title', title.get('title')),
                ('link', hardcoded + title.get('href')),
                ('duration', duration),
                ('thumb', img.get('data-src')),
                ('res', res),
                ('views', views[1:]),
                ('uploader', uploader),
                ('category', category),
                ('page', page)
                ]))

    return video_info


def play_video(_handle, video):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    soup = helper.get_soup(video)

    div = soup.find("div", id="video-player-bg")
    script_tag = div.find_all("script")[4]

    tmp = script_tag.string.split("setVideoHLS('")[-1]
    m3u_link = tmp.split("')", 1)[0]

    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=m3u_link)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

