#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from apps.timeline import TimeLine
from apps.tools import session
import dboperator

class RootHandler(BaseHandler):
    def get(self):
	self.dbase = dboperator.DB()
	stra = list(self.dbase.find(data="all"))
	l=len(stra)/2
	entries1=[]
	entries2=[]
	for i in range(l):
		entries1.append(stra[i])
		entries2.append(stra[i+l])
	#handler data for outputing
	self.render("index.html", entries1=entries1, entries2=entries2, entries=stra)

class TestHandler(BaseHandler):
    def get(self):
        self.render("test.html")

class FeedbackHandler(BaseHandler):
    
    def get(self):
        tl = TimeLine()
        r = tl._api.list()
        if r[0]:
            return self.render("feedback.html", **{'fb_list': r[1]})
        else:
            return self.render("feedback.html", **{'warning': r[1]})
    
    @session
    def post(self):
        uid = self.SESSION['uid']
        c = self.get_argument('content', None)
        n = self.get_secure_cookie("user") if uid else u'匿名驴友'
        tl = TimeLine()
        r = tl._api.save(owner=uid, column=u'weibo', subject=u'feedback', content=c, nick=n)
        if r[0]:
            return self.redirect("/feedback")
        else:
            return self.render("feedback.html", **{'warning': r[1]})

class Error404Handler(BaseHandler):
    def get(self):
        self.render("404.html")
    
class GoogleWebMasterHandler(BaseHandler):
    def get(self):
        self.write('google-site-verification: google9f2d915bcc519f6e.html')
    
    
    
    
    
    
    
    
    
