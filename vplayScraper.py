import re

class Scrap:

    def scrapFavorite(self, page):
        pos = page.find("<h2>Colec");
        if pos == -1:
            return [];
        page = page[:pos]
        print page
        match=re.compile('<a href="(/c/.+?/)" title="(.+?)"><span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page);
        return match

    def scrapSearch(self, page):
        match=re.compile('<a href="(/serials/browse.do\?sid=[0-9]+)" target="_top" class="group-item"(.+?)title="(.+?)"><img src="(.+?)" width="312" height="103" />(.+?)</a>').findall(page)
        return match
        
    def scrapSerials(self, page):
        print "Scrap Seriale"
        pos = page.find("<h2>Colec");
        if pos == -1:
            return [];
        page = page[pos:]
        match=re.compile('<a href="(/c/.+?/)" title="(.+?)"><span class="coll_poster" title="(.+?)" style="background-image:url\((.+?)\);"></span>').findall(page);
        return match
        
    def scrapSeasons(self, page):
        match=re.compile('href="(/c/.+?/\d+/)"><span>(Sezonul \d+)</span>').findall(page)
        return match
        
    def scrapEpisodes(self, page):
        #match=re.compile('<a href="(.+?)" class="serials-item"( style="margin-right: 0;")?><img src="(.+?)" width="160" height="85">( <div class="iswat" title="Watched"><img src="http://i.vplay.ro/ic/tick16.png"></div> )?(.+?)( <div class="isusb" title="Subtitrari">SUB</div>)?</a>').findall(page)
        match = re.compile('<a href="(.+?)" title="(.+?)" class="coll-episode-box">\s*<span class="thumb" style="background-image:url\((.+?)\);"></span>\s*<span class="title" title="(.+?)">(.+?)</span>').findall(page);
        print match[0]
        return match
        
    def scrapEpisodeId(self, page):
        match=re.compile('http://vplay.ro/watch/(.+?)/').findall(page)
        return match
        
    def scrapLastPage(self, page):
        match=re.compile('href="/c/1g6g9v5m/2/"><span>Sezonul 2</span>').findall(page)
        print "TESTTTTT"
        print page
        print match
        return match
