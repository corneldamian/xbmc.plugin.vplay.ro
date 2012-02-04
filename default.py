import sys, xbmcaddon, xbmcplugin, urllib, urllib2, xbmcgui
import res, time


# plugin constants
__version__ = "1.0"
__plugin__ = "Vplay" + __version__
__url__ = "www.xbmc.com"

# xbmc hooks
__settings__ = xbmcaddon.Addon(id='plugin.video.vplay')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting("debug") == "true"


def OPTIONS():
    re = vplayBrowser.ListResources();
    addDir('Favorite', res.urls['serials'], 4, re.get_thumb('favorite'), 6)
    addDir('Seriale', res.urls['serials'], 1, re.get_thumb('seriale'), 30)
    if __settings__.getSetting('last_movie'):
    	import simplejson as json
    	movie = json.loads(__settings__.getSetting('last_movie'))
        addDir(movie['name'], movie['url'], 6, re.get_thumb('last'), 0)    
    addDir('Search','http://vplay.ro/serials/?s', 5, re.get_thumb('search-icon'), 0)    
    addLink('Login','http://vplay.ro/login/', re.get_thumb('login') , 'login')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def SERIAL(page=None, type=None, search=None):
    #print "SERIAL: page: " + str(page) + " type: " + str(type) + " search: " + str(search)
    if page == None:
        page = 1
    try:
        page = int(page)
    except:
        page = 1
        
    browser = vplayBrowser.ListResources()
    lst = browser.getSerials(page=page, type=type, search=search)
    last_page = browser.getLastPage()
    for i in lst:
        main = res.urls['main']
        url = main + str(i[0])

        addDir(i[1],url, 2, i[3])
    
    page += 1
    mode = 1;
    if search != None:
	mode = 5
    if page < last_page:
        t = browser.get_thumb('next')
        addNext('Next',page, 5, t)
    
    xbmc.executebuiltin("Container.SetViewMode(500)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]

    return param


def VIDEOLINKS(url,name):
    print url
    browser = vplayBrowser.ListResources()
    lst = browser.getEpisodes(url)
    for i in lst:
        url = res.urls['main']
        url = url + str(i[0])
        if len(i[-3]) > 0:
            name = str(i[-2]) + " (Watched)"
        else:
            name = str(i[-2])
        if len(i[-1]) > 0:
            name = name + "(Subed)"
        addLink(name, url, i[2], 'play_video')
    
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)


def SEZON(url, name):
    import simplejson as json
    movie = json.dumps({"name": name, "url": url})
    __settings__.setSetting('last_movie', movie)
    browser = vplayBrowser.ListResources()
    lst = browser.getSesons(url)
    for i in lst:
        url = res.urls['browse']
        url = url + str(i[0])
        addDir(i[-1],url, 3, '')
    
    xbmc.executebuiltin("Container.SetViewMode(550)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def addNext(name,page,mode,iconimage):
    u=sys.argv[0]+"?url="+str(page)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir(name,url,mode,iconimage, len = 0):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems = len)
    return ok

def addLink(name,url,iconimage,action):
    ok=True
    url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+ str(action) + "&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def checkVideoLink(url):
    return url
    import vplayCommon
    resp = urllib2.urlopen(vplayCommon.HeadRequest(url))
    newurl = resp.geturl();
    if newurl != url:
	print "CHECK URL: OLD VIDEO URL: " + url
	print "CHECK URL: NEW VIDEO URL: " + newurl
    return newurl

def startPlugin():
    params=get_params()
    url=None
    name=None
    mode=None
    action=None

    try:
            url=urllib.unquote_plus(params["url"])
    except:
            pass
    try:
            name=urllib.unquote_plus(params["name"])
    except:
            pass
    try:
            mode=int(params["mode"])
    except:
            pass
    try:
        action = str(params['action'])
    except:
        pass

    print "Mode: "+str(mode)
    print "URL: "+str(url)
    print "Name: "+str(name)
    print "Handle: "+sys.argv[1]


    if mode==None or url==None or len(url)<1:
        if action == None:
            #print "mode 0"
            OPTIONS()
            __login__.login(login=True)
    elif mode==1 and action==None:
        #print "mode 1"
        SERIAL(url, "Categorii")
    elif mode==2 and action==None:
        #print "mode 2"
        SEZON(url, name)
    elif mode==3 and action==None:
        #print "mode 3"
        VIDEOLINKS(url,name)
    elif mode==4 and action==None:
        #print "mode 3"
        SERIAL(url, "Favorite")
    elif mode==5:
	if url.isdigit():
		SERIAL(url, "Search", __settings__.getSetting( "search" )); 
	else:
        	__search__.search()
		if __search__.getResponse() != None:
            		SERIAL(None, "Search", __search__.getResponse() )
    elif mode==6 and action==None:
        #print "mode 6"
        SEZON(url, name)

        
    if action == 'play_video':
        details = __link__.getRealLink(url)
        print details

	details['url'] = checkVideoLink(details['url'])

        player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ) 
        player.play(details['url'])
        while not player.isPlaying():
            time.sleep(1)
            
        #print "DEFAULT: -->" + str(details['subs'])
        s = None
        if 'ro' in details['subs']:
            s = details['subs']['ro']
        elif 'en' in details['subs']:
            s = details['subs']['en']
        if s != None:
            player.setSubtitles(s)
    elif action == 'login':
        __login__.login(display=True)


if (__name__ == "__main__" ):
    import login, search
    __search__ = search.Search()
    __login__ = login.Login()
    import vplayBrowser
    import vplayCommon
    import vplayScraper
    __link__ = vplayBrowser.linkResolution()
    startPlugin()


