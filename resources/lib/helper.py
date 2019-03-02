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
Create a URL for calling the plugin recursively from the given set of keyword arguments.

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
#         list_categories       #
#################################
'''
Create the list of video categories in the Kodi interface.
'''
def list_categories(_url, _handle, categories):
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'My Video Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get video categories
    
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['category'])
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category['category'],
                                    'genre': category['category'],
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(_url, action='listing', category=category['category'], link=category['link'], page=1)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


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
    ##############################################
    #                Next
    if next == True:
        list_item = xbmcgui.ListItem(label='Next')
    
        url = get_url(_url, action='next', link=link, page=page ,category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    #
    #############################################

    # Iterate through videos.
    for video in videos:
        #set resolution Tag if res is available
        if video['res'] != '':
            title = '[' + video['res'] + '] ' + video['title'] 

        else:
            title = video['title']

        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=title)
        # builduing the description from views and uploader
        plot = "Views: " + str(video['views']) + "\nUploader: " + str(video['uploader'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': title, 
                                    'sorttitle': video['title'],
                                    'duration': video['duration'],
                                    'plot': plot,
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'poster': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(_url, action='play', video=video['link'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add sort methods for the virtual folder items 
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DURATION)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)