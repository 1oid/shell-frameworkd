# coding:utf-8
import requests

class Exploit:

    def attack(self, url):
        target = url + "/website-rank/getVoteRecordByManuscriptId.action"
        response = requests.get(target)
        if response.status_code == 200:
            return "The {} seems like Struct site.".format(target)