# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 02.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmcgui
import xbmcplugin
import resources.lib.xvideos as xvideos
import resources.lib.helper as helper
from urlparse import parse_qsl

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]

# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

if __name__ == '__main__':
    
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    paramstring = sys.argv[2][1:]

    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    #xbmc.log(str(params),level=xbmc.LOGNOTICE)

    # Check the parameters passed to the plugin give new and restart 
    # quit() is needed at the end of each if 

    #################################
    #           1st Start           #
    #################################
    if params == {}:
        # Catergorys
        list_item = xbmcgui.ListItem(label='Categories')
        url = helper.get_url(_url, action='category')
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        # Search
        list_item = xbmcgui.ListItem(label='Search')
        url = helper.get_url(_url, action='search')
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        # endOfDirectory
        xbmcplugin.endOfDirectory(_handle)
        quit()

    #################################
    #           listing             #
    #################################
    if params['action'] == 'listing':
        # Display the list of videos in a provided category.
        videos = xvideos.get_vids(params['link'], params['category'])
        has_next = False
        helper.list_videos(_handle, _url, videos, params['link'], params['category'], has_next)
        quit()

    #################################
    #             play              #
    #################################
    if params['action'] == 'play':
        # Play a video from a provided URL.
        xvideos.play_video(_handle, params['video'])
        quit()

    #################################
    #            search             #
    #################################
    if params['action'] == 'search':
        s_therm = helper.get_search()
        link = 'https://www.xvideos.com/?k=' + s_therm
        videos = xvideos.get_vids(link, 'search')
        has_next = True
        helper.list_videos(_handle, _url, videos, link, 'search', has_next)
        quit()

    #################################
    #            category           #
    #################################
    if params['action'] == 'category':
        categories = xvideos.get_cats()
        helper.list_categories(_url, _handle, categories)
        quit()

    #################################
    #              next             #
    #################################
    if params['action'] == 'next':
        # ads a &p= at first and raises the page number every call
  
        if params['page'] == '1':
            url = params['link'] + '&p=' + str(params['page'])
        else:     
            url = params['link'] + str(params['page'])
    
        page = int(params['page']) + 1
        videos = xvideos.get_vids(url, params['category'])
        has_next = True
        helper.list_videos(_handle, _url, videos, url, params['category'], has_next, page )
        quit()

    #################################
    #             error             #
    #################################
    # If the provided paramstring does not contain a supported action
    # we raise an exception. This helps to catch coding errors,
    # e.g. typos in action names.
    raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    quit()
