from flask import request

class UserInfo:
    def __init__(self, sessioninfo):
        #note this all very temporary for debug user, needs to redesigned for real auhtentication\
        # but this hides tyhis process behind a class
        self.username = 'undefined'
        if sessioninfo != None and sessioninfo.authorization != None:
            self.username = sessioninfo.authorization['username']
    
    def __eq__(self, other):
        if not isinstance(other, UserInfo):
            return NotImplemented
        
        return self.username == other.username

