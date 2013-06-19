import vplayCommon, login, vplayScraper, search
import res
import xbmc
import sys
import random
import simplejson as json
import codecs
import os

class ListResources:
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__" ].__plugin__
    __dbg__ = sys.modules[ "__main__" ].__dbg__
    __login__ = sys.modules[ "__main__" ].__login__
    __search__ = sys.modules[ "__main__" ].__search__
    
    def get_thumb(self, name):
        THUMBNAIL_PATH = os.path.join( self.__settings__.getAddonInfo('path'), "thumbnails" )
        p = os.path.join(THUMBNAIL_PATH, str(name) + '.png')
        if os.path.isfile(p):
            return p
        return ""
    
    def __init__(self):
        self.http_lib = vplayCommon.Http()
        self.session = None
        if not self.__settings__.getSetting( "username" ) or not self.__settings__.getSetting( "pwd" ):
            self.__login__.login()
        self.scrap = vplayScraper.Scrap()
    
    
    def getLastPage(self):
        last_page = 110;
#        p = self.http_lib._get(res.urls['serials'])
#        print "PAGE ==>" + str(p['httpcode'])
#        if p['httpcode'] == 200:
#            last_page = self.scrap.scrapLastPage(p['httpmsg'])
#            print "PAGE ==> " + str(last_page)
#        else:
#            last_page = 1
#        if len(last_page) > 0:
#            try:
#                last_page = int(last_page[0][0])
#            except:
#                last_page = 1
        return last_page

    def _get_session(self):
        val = self.__settings__.getSetting('session')
        val = val+"; promo_shown=1"
        xbmc.log("using session "+val)
        return val;
        
    def getSerials(self, page=None, type=None, search=None):
        self.session = self._get_session()
        if not self.session:
            self.__login__.login()
            self.session = self._get_session()
        
        if page == None:    
            url = res.urls['serials']
        else:
            try:
                int(page)
	        url = res.urls['serials'] + "/" + str(page) + "/"
            except:
                url = res.urls['serials']
	if type == "Search":
            url = res.urls['search'] + search

        cookie = str(self.session)
        lst = [];
        ret = self.http_lib._get(url, cookie)
        if ret['httpcode'] == 200:
            if type == None or type == "Categorii":
                lst = self.scrap.scrapSerials(ret['httpmsg'])
            elif type == "Favorite":
                lst = self.scrap.scrapFavorite(ret['httpmsg'])
            elif type == "Search":
                lst = self.scrap.scrapSearch(ret['httpmsg'])
		if len(lst) < 1 and int(page) == 1:
		    self.__search__.noResult();
            else:
                lst = self.scrap.scrapSerials(ret['httpmsg'])
        elif ret['httpcode'] == 301:
            self.__login__.login()
        else:
            raise IOError('Could not get serial list: %s --> %s' % (ret['httpcode'], ret['httpmsg']))

        return lst
        
    def getSesons(self, url):
        self.session = self._get_session()
	xbmc.log("getting sessons "+self.session);
        if not self.session:
            self.__login__.login()
            self.session = self._get_session()
            
        cookie =  str(self.session)
        ret = self.http_lib._get(url, cookie)
        lst = [];
        if ret['httpcode'] == 200:
            lst = self.scrap.scrapSeasons(ret['httpmsg'])
        elif ret['httpcode'] == 301:
            self.__login__.login()
        else:
            raise IOError('Could not get serial list: %s --> %s' % (ret['httpcode'], ret['httpmsg']))
        return lst
        
        
    def getEpisodes(self, url):
        self.session = self._get_session()
        if not self.session:
            self.__login__.login()
            self.session = self._get_session()
            
        cookie =  str(self.session)
        ret = self.http_lib._get(url, cookie)
        lst = [];
        if ret['httpcode'] == 200:
            lst = self.scrap.scrapEpisodes(ret['httpmsg'])
        elif ret['httpcode'] == 301:
            self.__login__.login()
        else:
            raise IOError('Could not get serial list: %s --> %s' % (ret['httpcode'], ret['httpmsg']))
        
        return lst
            
    def getFavorites(self, url):
        self.session = self._get_session()
        if not self.session:
            self.__login__.login()
            self.session = self._get_session()
            
        cookie =  str(self.session)
        ret = self.http_lib._get(url, cookie)
        lst = [];
        if ret['httpcode'] == 200:
            lst = self.scrap.scrapFavorites(ret['httpmsg'])
        elif ret['httpcode'] == 301:
            self.__login__.login()
        else:
            raise IOError('Could not get serial list: %s --> %s' % (ret['httpcode'], ret['httpmsg']))
        
        return lst        


class linkResolution:
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__" ].__plugin__
    __dbg__ = sys.modules[ "__main__" ].__dbg__
    __login__ = sys.modules[ "__main__" ].__login__
    
    def __init__(self):
        self.http_lib = vplayCommon.Http()
        self.scrap = vplayScraper.Scrap()
        self.random = random.random()
        
        #try:
        #    cur_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        #    cur_dir = os.path.join(cur_dir, 'subtitles')
        #    if os.path.isdir(cur_dir) is False:
        #        os.makedirs(cur_dir)
        #    self.subs_dir = cur_dir
        #except:
        tmp_dir = xbmc.translatePath( "special://temp")
        subs = os.path.join(tmp_dir, 'plugin.video.vplay_subtitles')
        if os.path.isdir(subs) is False:
            os.makedirs(subs)
        self.subs_dir = subs

    def _get_session(self):
        val = self.__settings__.getSetting('session')
        val = val+"; promo_shown=1"
        xbmc.log("using session "+val)
        return val;
            
    def convert_time_to_something(self, f):
        f = int(f)
        def min_and_sec(f):
            if f > 60:
                f_minute = f/60
                f_secunde = f%60
            else:
                f_minute = "00"
                f_secunde = f
            
            if f_minute < 10:
                f_minute = "0" + str(f_minute)
            if f_secunde < 10:
                f_secunde = "0" + str(f_secunde)
            return str(f_minute) + ":" + str(f_secunde) + ",0"

        if f > 3600:
            hours = f/3600
            f = f%3600
            if hours < 10:
                hours = "0" + str(hours)
            else:
                hours = str(hours)
        else:
            hours = "00"
        
        final = hours + ":" + min_and_sec(f)
            
        return final

    def getSubs(self, key, subs):
        url = res.urls['sub'] + '?' + str(self.random)
        ret = {}
        sub_dir = os.path.join(self.subs_dir, str(key))
        if os.path.isdir(sub_dir) is False:
            try:
                os.makedirs(sub_dir)
            except Exception, err:
                return ret
                
        for i in subs:
            print "SUBS: Processing " + str(i)
            sub_file_name = os.path.join(sub_dir, str(i) + '.sub')
            
            if os.path.isfile(sub_file_name) is True:
                ret[str(i).lower()] = sub_file_name
                continue
                
            postData = {"key": str(key), "lang":  str(i)}
            url_ret = self.http_lib._post(url, postData)
            
            if url_ret['httpcode'] != 200:
                print "SUBS: got code " + str(url_ret['httpcode'])
                continue
                
            data = url_ret['httpmsg'].strip('&subsData=').rstrip('\n')
            try:
                data = data.expandtabs(2);
                obj = json.loads(data)
                fisier = codecs.open(sub_file_name, 'w', 'utf-8')
                count = 1
                for j in obj:
                    sub_line = str(count) + '\n'
                    f = int(j['f'])
                    t = int(j['t'])
                    
                    sub_line = sub_line + self.convert_time_to_something(f) + " --> " + self.convert_time_to_something(t) + '\n'
                    sub_line = sub_line + j['s'] + '\n\n'
                    
                    fisier.write(sub_line)
                    count = count + 1
                fisier.close()
            except Exception, err:
                print "SUBS: Got exception " + str(err)
                continue
            ret[str(i).lower()] = sub_file_name
        return ret

    def processDinosaur(self, key):
        url = res.urls['dino']
        #+ '?key=' + str(key) + "&rand=" + str(self.random)
        postData = {"key": str(key)}
        ret = self.http_lib._post(url, postData)
        print 'DINO URL: ' + str(url)
        print "DINO: ",  ret
        if ret['httpcode'] != 200:
            raise Exception('Could not get movie link')
        
        #print "XXXXXX ==> " +  str(ret)
        vals = ret['httpmsg'].split('&')
        attrs = {}
        for i in vals:
            if len(i) == 0:
                continue
            value = i.split('=')
            attrs[value[0]] = value[1]
        return attrs
            
    def getRealLink(self, url):
        self.session = self._get_session()
        if not self.session:
            self.__login__.login()
            self.session = self._get_session()
        
        cookie =  str(self.session)
        ret = self.http_lib._get(url, cookie)
        
        if ret['httpcode'] == 301 or ret['httpcode'] == 302:
            __login__.login()
            self._get_session()
            ret = self.http_lib._get(url, cookie)
        
        if ret['httpcode'] != 200:
            raise Exception('failed to get episode: %s' % (ret['httpcode']))
            
        ep_id = self.scrap.scrapEpisodeId(url)
        if len(ep_id) != 1:
            raise ValueError('Could not get episode ID')
        
        values = self.processDinosaur(ep_id[0])
        if len(values) == 0:
            raise IOError('Could not get movie link')
            
        try:
            s = json.loads(values['subs'])
        except Exception, err:
            print "SUBS: Got exception in json " + str(err)
            s = []
            
        print "SUBS: ---> " + str(s)
        subs = self.getSubs(ep_id[0], s)
        ret = {'url': values['nqURL'], 'subs': subs}
        return ret     
