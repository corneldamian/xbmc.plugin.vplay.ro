'''
    Vplay.ro plugin for XBMC
'''

import sys, xbmcaddon, xbmcplugin, urllib, urllib2, xbmcgui
import res, time


# plugin constants
__version__ = "1.0"
__plugin__ = "Vplay" + __version__
__author__ = ""
__url__ = "www.xbmc.com"

# xbmc hooks
__settings__ = xbmcaddon.Addon(id='plugin.video.vplay')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting("debug") == "true"


def OPTIONS():
    addDir('Favorite', res.urls['serials'], 4, '')
    addDir('Seriale', res.urls['serials'], 1, '')
    addLink('Search','http://vplay.ro/serials/','', 'search')    
    addLink('Login','http://vplay.ro/login/','', 'login')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

def SERIAL(page=None, type=None):
    if page == None:
        page = 1
    try:
        page = int(page)
    except:
        page = 1
        
    browser = vplayBrowser.ListResources()
    lst = browser.getSerials(page=page, type=type)
    last_page = browser.getLastPage()
    print "DEFAULT: " + str(last_page)
    for i in lst:
        main = res.urls['main']
        url = main + str(i[0])
        addDir(i[2],url, 2, i[3])
    
    page += 1
    if page < last_page:
        t = browser.get_thumb('next')
        addNext('Next',page, 1, t)
    
    xbmc.executebuiltin("Container.SetViewMode(500)") 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    print paramstring
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


def SEZON(url):
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

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


def addLink(name,url,iconimage,action):
    ok=True
    url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+ str(action) + "&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def startPlugin():
    params=get_params()
    print params
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


    if mode==None or url==None or len(url)<1:
        if action == None:
            print "mode 0"
            OPTIONS()
    elif mode==1 and action==None:
        print "mode 1"
        SERIAL(url, "Categorii")
    elif mode==2 and action==None:
        print "mode 2"
        SEZON(url)
    elif mode==3 and action==None:
        print "mode 3"
        VIDEOLINKS(url,name)
    elif mode==4 and action==None:
        print "mode 3"
        SERIAL(url, "Favorite")

        
    if action == 'play_video':
        details = __link__.getRealLink(url)
        player = xbmc.Player()
        
        player.play(details['url'])
        while not player.isPlaying():
            time.sleep(1)
            
        print "DEFAULT: -->" + str(details['subs'])
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
    import login
    __login__ = login.Login()
    __login__.login(login=True)
    import vplayBrowser
    import vplayCommon
    import vplayScraper
    __link__ = vplayBrowser.linkResolution()
    startPlugin()

