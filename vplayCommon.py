#import pycurl
#import os
#import StringIO
#import xbmc, sys
#import vplayScraper
import urllib, urllib2


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301( 
            self, req, fp, code, msg, headers)              
        result.status = code
        print code                               
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):   
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result

class HeadRequest(urllib2.Request):
   def get_method(self):
	return "HEAD"

class Http:

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/15.0.847.0 Chrome/15.0.847.0 Safari/535.1'
        self.headers = {}

    def _get(self, url, cookie=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.user_agent)
        if cookie != None:
            req.add_header('Cookie', str(cookie))
        opener = urllib2.build_opener(SmartRedirectHandler())
        try:
            page = opener.open(req)
        except urllib2.URLError, e:
            return {'httpcode': e.code, 'httpmsg': '', 'cookie': None}
        response=page.read()
        page.close()
        try:
            cookie = page.info()['Set-Cookie']
            s = str(cookie).split(';')
            for i in s:
                n_s = i.split('=')
                if len(n_s) != 2:
                    continue
                if str(n_s[0]) == 'PHPSESSID':
                    cookie = i
        except:
            cookie = None
        try:
            c = page.status
        except:
            c = 200
        return {'httpcode': c, 'httpmsg': response, 'cookie': cookie}
        
        
    def _post(self, url, data, cookie=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.user_agent)
        if cookie != None:
            req.add_header('Cookie', str(cookie))
        p = urllib.urlencode( data )
        req.add_data(p)
        opener = urllib2.build_opener(SmartRedirectHandler())
        try:
            page = opener.open(req)
        except urllib2.URLError, e:
            return {'httpcode': e.code, 'httpmsg': '', 'cookie': None}
        response=page.read()
        page.close()
        try:
            cookie = page.info()['Set-Cookie']
            s = str(cookie).split(';')
            for i in s:
                n_s = i.split('=')
                if len(n_s) != 2:
                    continue
                if str(n_s[0]) == 'PHPSESSID':
                    cookie = i
        except:
            cookie = None
            
        try:
            c = page.status
        except:
            c = 200
        return {'httpcode': c, 'httpmsg': response, 'cookie': cookie}
    
    
"""
class Http:

    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if os.access(cur_dir, os.W_OK):
            self.cookie = os.path.join(cur_dir, 'cookie.txt')
        else:
            self.cookie = os.path.join( xbmc.translatePath( "special://temp"), 'plugin.video.vplay_cookie.txt' )
            
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.HEADER, 0)
        self.c.setopt(pycurl.BUFFERSIZE, 0)
        self.c.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.c.setopt(pycurl.TIMEOUT, 120)
        self.c.setopt(pycurl.COOKIEJAR, self.cookie)
        self.c.setopt(pycurl.COOKIEFILE, self.cookie)
        self.c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/15.0.847.0 Chrome/15.0.847.0 Safari/535.1')
        
        
    def _post(self, url, data, cookie=None):
        b = StringIO.StringIO()
        attr = {}
        self.c.setopt(self.c.URL, url)
        self.c.setopt(pycurl.CUSTOMREQUEST, "POST")
        self.c.setopt(pycurl.POSTFIELDS, data)
        self.c.setopt(self.c.WRITEFUNCTION, b.write)
        if cookie != None:
            self.c.setopt(pycurl.COOKIE, cookie)
        self.c.perform()
        httpCode = self.c.getinfo(pycurl.HTTP_CODE)
        attr['httpcode'] = httpCode
        attr['httpmsg'] = b.getvalue()
        return attr
        
    def _get(self, url, cookie=None):
        b = StringIO.StringIO()
        attr = {}
        self.c.setopt(self.c.URL, url)
        self.c.setopt(pycurl.CUSTOMREQUEST, "GET")
        self.c.setopt(self.c.WRITEFUNCTION, b.write)
        if cookie != None:
            self.c.setopt(pycurl.COOKIE, cookie)
        self.c.perform()
        httpCode = self.c.getinfo(pycurl.HTTP_CODE)
        attr['httpcode'] = httpCode
        attr['httpmsg'] = b.getvalue()
        return attr
"""
