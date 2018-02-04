# coding:utf-8
import os
import sys
from spider.baiduspider import *
from spider.oshadan import *
from urlparse import urlparse
# from spider.zoomeye import *
import requests

banner = '''
  ______                     __          __        _    
 |  ____|                    \ \        / /       | |   
 | |__ _ __ __ _ _ __ ___   __\ \  /\  / /__  _ __| | __
 |  __| '__/ _` | '_ ` _ \ / _ \ \/  \/ / _ \| '__| |/ /
 | |  | | | (_| | | | | | |  __/\  /\  / (_) | |  |   < 
 |_|  |_|  \__,_|_| |_| |_|\___| \/  \/ \___/|_|  |_|\_\
'''
sys.path.append(os.getcwd()+'/plugins')

# url 数据采集接口
class spiderEngine(object):

    def __init__(self):
        # self.keyword = keyword
        # self.page = page
        self.oshadanapi = oshadan()
        # self.oshadanLogin = self.oshadanapi.login()

    # 百度爬虫接口
    def baiduspider(self, keyw, page=1):
        retLists = keyword(keyw, page)
        return map(lambda x: "http://{}".format(urlparse(x).netloc), map(location, retLists))

    # oshadan数据采集接口
    def oshadanspider(self, keyword, page=1):
        if self.oshadanLogin:
            retList = self.oshadanapi.search(keyword, page)
            return map(lambda x: "http://{}".format(urlparse(x).netloc), map(lambda x:x["url"], retList))

    # zoomeye数据采集接口
    '''def zoomeyespider(self, keyword, page=1):
        retList = Zoomeye(query=keyword, page=page).get()
        return map(lambda x: "http://{}".format(x), retList)
       '''

# print "xx"
# print spiderEngine("metinfo", 2).oshadanspider()

class shellframework(object):

    plugins = []

    def __init__(self, pluginName, outputFile=None):
        self.pluginName = pluginName
        self.load_plugins()
        self.output = outputFile
        print "Load Plugin: {}".format(self.pluginName)

    # 加载所有插件
    def load_plugins(self):
        self.plugins = os.listdir(os.getcwd()+'/plugins')

    # 判断插件是否存在
    def exist_plugin(self):
        return self.pluginName+'.py' in self.plugins

    # 调用解析插件
    def exec_plugin(self, url):
        if not self.exist_plugin():
            print "The plugin does not exist"
            exit(0)

        md = __import__(self.pluginName)
        try:
            if hasattr(md, 'Exploit'):
                exp = getattr(md, 'Exploit')()
                ret = exp.attack(url)
                if ret:
                    print ret
                    if self.output:
                        with open(self.output, 'a') as f:
                            f.write(ret+'\n')
            else:
                print "Plugin Error"
        except Exception as e:
            print e

# a = shellframework("metinfo_sql")
# # print a.plugins
# a.exec_plugin("http://gj158.com/")

# 列出所有插件
def listPlugView(pluginLike=None):
    def load_plugins():
        plugins = os.listdir(os.getcwd() + '/plugins')
        return filter(lambda x:(True, False)['pyc' in x or '__init' in x], plugins)

    plugins = load_plugins()
    if pluginLike:
        plugins = filter(lambda x: re.search(pluginLike, x), plugins)
    return plugins

# 解析命令参数
def cmdparse(engine, keyword, page, plugin, list=None, output=None, filename=None):
    print banner
    retspider = []
    if list:
        plugins = listPlugView() if list=="all" else listPlugView(list)
        print "List Plugins: "
        for p in plugins:
            print p[:-3]
        exit(0)

    if engine and keyword and page and plugin or filename:
        print "Spider Engine: " + engine if engine else "Read Filename: " + filename
        page = str(page).split("-")
        pageIntSta = 1 if len(page) == 1 else int(page[0])
        pageIntEnd = int(page[-1])

        if engine: print "Spider from page {} to page {}".format(pageIntSta, pageIntEnd)
        # 判断采集接口并返回数据
        engineApi = spiderEngine()
        if engine == "baidu":
            for p in range(pageIntSta, pageIntEnd+1):
                map(lambda x:retspider.append(x), engineApi.baiduspider(keyword, p))
        elif engine == "oshadan":
            for p in range(pageIntSta, pageIntEnd+1):
                map(lambda x: retspider.append(x), engineApi.oshadanspider(keyword, p))
        #elif engine == 'zoomeye':
        #    for p in range(pageIntSta, pageIntEnd+1):
        #        map(lambda x: retspider.append(x), engineApi.zoomeyespider(keyword, p))
        elif filename:
            with open(filename) as f:
                lines = f.readlines()
            map(lambda x: retspider.append(x.strip()), lines)
        else:
            print "Error Engine! Retry!"

        print "Date total: "+str(len(retspider))

        pg = shellframework(plugin, output)
        for url in set(retspider):
            try:
                pg.exec_plugin(url)
            except requests.ConnectionError:
                continue
            except requests.TooManyRedirects:
                continue

if __name__ == '__main__':
    from optparse import OptionParser

    usage = '%prog -k "inurl:/news/shownews.php?lang=cn&id=" -p 2 -e baidu -l metinfo_sql\n'
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--keyword", dest="keyword", help="Waiting for collection's command.")
    parser.add_option("-p", "--page", dest="page", help="Collected pages.", default=10)
    parser.add_option("-e", "--engine", dest="engine", help="Spider Engine", default=None)
    parser.add_option("-l", "--load", dest="load", help="Load Plugin Script Name", type="string", default=None)
    parser.add_option("-s", "--scripts", dest="scripts", help="List Plugin", type="string", default=None)
    parser.add_option("-o", "--output", dest="output", help="Output file", type="string", default=None)
    parser.add_option("-f", "--filename", dest="filename", help="Read file", type="string", default=None)
    options, args = parser.parse_args()

    cmdparse(options.engine, options.keyword, options.page, options.load, options.scripts, options.output, options.filename)
