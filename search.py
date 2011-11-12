import xbmc, sys
#import pycurl
import StringIO
import os
import res
import re
import vplayCommon
import xbmcgui

class Search(xbmcgui.Window):
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__" ].__plugin__
    __dbg__ = sys.modules[ "__main__" ].__dbg__
    search_url = res.urls['search']
    
    def __init__(self):
        self.http_lib = vplayCommon.Http()
	self.response = None
    
    def search(self):
        search = self.__settings__.getSetting( "search" )

    	self.strActionInfo = xbmcgui.ControlLabel(100, 120, 200, 200, '', 'font13', '0xFFFF00FF')
    	self.addControl(self.strActionInfo)
    	self.strActionInfo.setLabel('Push BACK to quit')
    	self.strActionInfo = xbmcgui.ControlLabel(100, 300, 200, 200, '', 'font13', '0xFFFFFFFF')
    	self.addControl(self.strActionInfo)

    	keyboard = xbmc.Keyboard(search)
    	keyboard.doModal()

    	if (keyboard.isConfirmed()):
		self.__settings__.setSetting( "search", keyboard.getText() )
		self.response = keyboard.getText()
        return 0

    def getResponse(self):
	return self.response

    def noResult(self):
        dialog = xbmcgui.Dialog()
	dialog.ok("No Search Result", " No movie found with name: " + self.response)
