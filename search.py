#!/usr/bin/env python3
## -*- coding:utf-8 -*-

import requests
import re
import json

timeout = 15

headers = {'X-Requested-With': 'XMLHttpRequest'}
r = requests.get("http://bbs.byr.cn/")


def assembleSectionUrl (index):
    return ("http://bbs.byr.cn/section/" + str(index) + "?_uid=guest")


def assembleBoardUrl (uid, relative_url):
    name = relative_url.split('/')
    return ("http://bbs.byr.cn/s/article?t1=&au=" + uid + "&b=" + name[2] + "&_uid=guest")


def getAllSections(r, url):
    sections = []
    try:
        r_sub = requests.get(url, cookies = r.cookies.get_dict(), headers = headers, timeout = timeout)
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        return sections
    j = json.loads (r_sub.text)

    for i in range(len(j)):
        tmp = re.findall(r'href="(.*?)">(.*?)</a>', j[i]['t'])
        node = {}
        node['url'] = tmp[0][0]
        node['name'] = tmp[0][1]
        node['len'] = 0
        sections.append (node)

    return sections


def getSectionList(r, url):
    try:
        r_sub = requests.get(url, cookies = r.cookies.get_dict(), headers = headers, timeout = timeout)
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        return ''
    content = re.findall (r'class=\"title_1\".*?href=\"(.*?)\">(.*?)</a>', r_sub.text)
    #print (content)
    return content


def getContentOfParticularBoard (r, url):
    try:
        r_sub = requests.get(url, cookies = r.cookies.get_dict(), headers = headers, timeout = timeout)
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        return ''
    items =  re.findall(r'<td.*?_9">.*?href="(.*?)">(.*?)</a>.*?_10">(.*?)</td>.*?_11 middle">(.*?)</td>', r_sub.text)
    return items


def iteration (uid, sections):
    del_list = []
    for i in range (len(sections)):
        section_url = assembleSectionUrl (i)
        section_list = getSectionList (r, section_url)
        #print (section_list)
        sections[i]['border'] = []

        for j in range (len(section_list)):
            print (section_list[j][1])
            border = {}
            border['url'] = section_list[j][0]
            border['name'] = section_list[j][1]

            board_url = assembleBoardUrl (uid, section_list[j][0])
            items  = getContentOfParticularBoard (r, board_url)
            if len(items) != 0:
                border['items'] = items
                sections[i]['border'].append (border)
                sections[i]['len'] = (int (sections[i]['len']) + 1)

        if int(sections[i]['len']) == 0:
            del_list.append (i)

    for i in range (len(del_list)):
        del (sections[del_list[i]-i])

    return sections


def search (uid):
    print (uid)
    sections = getAllSections (r, "http://bbs.byr.cn/section/ajax_list.json?uid=guest&root=list-section")
    return iteration (uid, sections)


if __name__ == "__main__":
    result = search ('doug')
    print (result)
