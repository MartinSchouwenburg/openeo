from flask import request

class UserInfo:
    def __init__(self, sessioninfo):
        #note this all very temporary for debug user, needs to redesigned for real auhtentication\
        # but this hides tyhis process behind a class
        self.username = 'undefined'
        if sessioninfo.authorization != None:
            self.username = sessioninfo.authorization['username']

