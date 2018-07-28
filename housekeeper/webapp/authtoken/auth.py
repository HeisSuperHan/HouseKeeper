import hashlib


class auth():

    def __init__(self,username,uuid):
        self.salt = 'jiaqinetwork'
        self.username = username
        self.uuid = uuid
        self.md5 = hashlib.md5()

    def create_cookies(self):
        self.md5.update(self.uuid.encode('utf-8'))
        cookies = self.md5.hexdigest()
        return cookies

    def create_token(self):
        '''
        token used to detect CSFR
        it created by username + uuid + salt
        '''
        a = self.username+self.uuid+self.salt
        self.md5.update(a.encode('utf-8'))
        token = self.md5.hexdigest()
        return token



