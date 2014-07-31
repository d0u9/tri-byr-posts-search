import search
import sys
import time
import webbrowser
import urllib
import platform

html = \
    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'\
    '<html xmlns="http://www.w3.org/1999/xhtml">'\
    '<head>'\
    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'\
    '<script type="text/javascript" src="jquery.js"></script>'\
    '<title>{#user}</title>'\
    '<style type="text/css">'\
    'body {font-family: "Lucida Grande", "Lucida Sans Unicode", Helvetica, Arial, Verdana, sans-serif;font-size: 16px}'\
    '.float-left {float: left;}'\
    '.float-right {float: right;}'\
    '.info {width: 960px;margin-left: auto;margin-right: auto;margin-top: 10px;}'\
    '.section-description {margin-top: 10px;height: 30px;line-height: 30px;font-size: 20px;}'\
    '.section {margin-left: auto;margin-right: auto;width: 960px;overflow: auto;padding-left: 20px;padding-right: 20px;}'\
    '.section-body {overflow: auto;border-right-width: thin;border-left-width: thin;border-right-style: solid;border-left-style: solid;border-right-color: #666;border-left-color: #666;}'\
    '.border {height: 26px;line-height: 26px;padding-left: 8px;width: 914;border-bottom-width: thin;border-bottom-style: dashed;border-bottom-color: #666;border-top-width: thin;border-top-style: solid;border-top-color: #666;font-weight: bold;}'\
    '.items-body {width: 958px;height: auto;}'\
    '.item {height: 23px;line-height: 23px;font-size: 14px;border-bottom-width: thin;border-bottom-style: solid;border-bottom-color: #666;}'\
    '.line {width: 20px;min-width: 20px;padding-left: 8px;font-size:20px;}'\
    '.title {width: 600px;padding-left:8px;padding-right:8px;}'\
    '.time {width: 100px;padding-left:8px;padding-right:8px;text-align:center;}'\
    '.re-amount {width: 80px;padding-left:8px;padding-right:8px;text-align:center;}'\
    '.space {height: 10px;}'\
    '.even-line {background-color: #E2E3FF;}'\
    '</style>'\
    '</head>'\
    '<body>{#body}</body>'\
    '</html>'

info = \
    '<div class="info"><span>查询用户：{#user}</span><span style="margin-left:20px">查询开始时间：{#time_start}</span><span style="margin-left:20px">查询结束时间：{#time_finish}</span></div><hr />'

section_t = \
    '<div class="section">'\
    '<div class="section-description">{#sec-des}</div>'\
    '<div class="section-body">'\
    '{#sec-body}'\
    '</div></div>'

border_t = \
    '<div class="border">{#border-name}</div>'\
    '<div class="items-body">'\
    '{#border-body}'\
    '</div><div class="space"></div>'

item_t = \
    '<div class="item{#colored}">'\
    '<div class="line float-left">☞</div>'\
    '<div class="title float-left"><a href="http://bbs.byr.cn/{#url}">{#title}</a></div>'\
    '<div class="re-amount float-right">{#re-amount}</div>'\
    '<div class="time float-right">{#time}</div>'\
    '</div>'

colored = ' even-line'



if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print ("usage: %s [username]" %sys.argv[0])
        sys.exit()

    time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = search.search (sys.argv[1])

    section = ''
    for s in range (len(result)):
        borders = result[s]['border']

        border = ''
        for b in range (len(borders)):
            items = borders [b]['items']

            item = ''
            for i in range (len(items)):
                item += item_t.replace ('{#title}', items[i][1])
                item = item.replace ('{#re-amount}', items[i][3])
                item = item.replace ('{#time}', items[i][2])
                item = item.replace ('{#url}', items[i][0])
                if (i % 2 == 0):
                    item = item.replace ('{#colored}', colored)
                else:
                    item = item.replace ('{#colored}', '')

            border += border_t.replace ('{#border-name}', borders[b]['name'])
            border = border.replace ('{#border-body}', item);
            border = border [0:-25]

        section += section_t.replace ('{#sec-des}', result[s]['name'])
        section = section.replace ('{#sec-body}', border)

    body = info + section
    html = html.replace ('{#body}', body)
    time_finish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    html = html.replace ('{#user}', sys.argv[1])
    html = html.replace ('{#time_start}', time_start)
    html = html.replace ('{#time_finish}', time_finish)

    file_name = sys.argv[1] + "_" + time_finish.replace(':', '_') + '.html'

    if (platform.system() == "Windows"):
        file_path = 'C:\TEMP' + file_name
    else:
        file_path = '/tmp/' + file_name

    f = open (file_path, 'w')
    f.write (html)
    f.close()

    print ("-------------------- complete --------------------------")
    print ("html file is saved in '%s'" %file_path)
    html_file = urllib.parse.quote (file_path)
    webbrowser.open ('file://' + html_file)

