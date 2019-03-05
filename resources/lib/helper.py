# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmc
import xbmcgui
import xbmcplugin
import requests
from urllib import urlencode
from bs4 import BeautifulSoup

#################################
#           get_soup            #
#################################
# takes a url and makes a soup
def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    req.close()
    return soup

#################################
#        convert_duration       #
#################################
# takes a duration like "1 h 53 min" and converts it to seconds.
def convert_duration(duration):
    if duration.find("h") != -1:  #
        h = int(duration[0])
        inta = duration[4:-4]
        minute = int(duration[4:-4]) + (h * 60)
        duration = minute * 60
        return duration #in seconds

    if duration.find("min") != -1:
        duration = int(duration[:-4]) * 60
        return duration #in seconds

    if duration.find("sec") != -1:
        duration = int(duration[:-4])
        return duration #in seconds

#################################
#           get_url             #
#################################
'''
Create a URL for calling the plugin recursively from the given set of
keyword arguments.

:param kwargs: "argument=value" pairs
:type kwargs: dict
:return: plugin call URL
:rtype: str
'''
def get_url(_url, **kwargs):
   return '{0}?{1}'.format(_url, urlencode(kwargs))


#################################
#           get_search          #
#################################
# opens a kodi text Dialog and returns the Input

def get_search():
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Search')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term  = kb.getText()
        return(search_term)
    else:
        return

#################################
#           list_videos         #
#################################
'''
Create the list of playable videos in the Kodi interface.
'''
def list_videos(_handle, _url, videos, link, category, next, page=1):
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, category)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

    # Iterate through videos.
    for video in videos:
        #set resolution Tag if res is available
        if video['res'] is not None:
            title = '[' + video['res'] + '] ' + video['title']
        else:
            title = video['title']

        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=title)
        # builduing the description from views and uploader
        plot = "Views: " + video['views'] + "\nUploader: "+ video['uploader']
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info correctly.
        list_item.setInfo('video', {'title': title,
                                    'sorttitle': video['title'],
                                    'duration': video['duration'],
                                    'plot': plot,
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, etc.) for the list item.
        list_item.setArt({'thumb': video['thumb'],
                          'icon': video['thumb'],
                          'poster': video['thumb'],
                          'fanart': video['thumb']})

        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=url
        url = get_url(_url, action='play', video=video['link'])
        is_folder = False

        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    if next is True:
        # Add the next button to the end of list
        list_item = xbmcgui.ListItem(label='Next')
        url = get_url(_url, action='next',
                      link=link, page=page ,category=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_UNSORTED)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)