import urllib
import urllib3

from bs4 import BeautifulSoup
import sys

class Robot(object):
    @classmethod
    def start(cls, url, postdata=None):
        print(url)
#        exit(0)
        if postdata != None:
            print("Posting not none dangit")
        user_agent = { 'user-agent' : 'Mozilla/5.0' }
        http = urllib3.PoolManager(10, headers=user_agent)

        response = http.request('GET', url, postdata)
        #print(response.data)
        soup = BeautifulSoup(response.data, 'lxml')
        return cls(url, soup)
    
    def __init__(self, url, html):
        self.url = url
        self.html = html
    
    @property
    def baseurl(self):
        if '?' in self.url:
            return self.url[:self.url.index('?')]
        else:
            return self.url
    
    def get_new_url(self, options):
        return self.baseurl + '?' + urllib.parse.urlencode(options)
