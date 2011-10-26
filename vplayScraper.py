import re


class Scrap:

    def scrapFavorite(self, page):
        match=re.compile('<a href="(/serials/browse.do\?sid=[0-9]+)" target="_top" class="group-item"(.+?)title="(.+?)"><img src="(.+?)" width="312" height="103">(.+?)</a>').findall(page)
        return match
        
    def scrapSerials(self, page):
        match=re.compile('<a href="(/serials/browse.do\?sid=[0-9]+)" target="_top"  class="group-item"(.+?)title="Seriale Online: (.+?)"><img src="(.+?)" width="312" height="103">(.+?)</a>').findall(page)
        return match
        
    def scrapSeasons(self, page):
        match=re.compile('<a href="(\?sid=[0-9]+&ses=([0-9]+)?)"( class="sel")?>(.+?)</a>').findall(page)
        return match
        
    def scrapEpisodes(self, page):
        match=re.compile('<a href="(.+?)" class="serials-item"( style="margin-right: 0;")?><img src="(.+?)" width="160" height="85">( <div class="iswat" title="Watched"><img src="http://i.vplay.ro/ic/tick16.png"></div> )?(.+?)( <div class="isusb" title="Subtitrari">SUB</div>)?</a>').findall(page)
        return match
        
    def scrapEpisodeId(self, page):
        match=re.compile('http://vplay.ro/watch/(.+?)/').findall(page)
        return match
        
    def scrapLastPage(self, page):
        match=re.compile('<a href="\?page=([0-9]+)" title="Ultimul" class="ppage" rel="([0-9]+)">').findall(page)
        return match
