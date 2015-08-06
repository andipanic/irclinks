#!/usr/bin/python

import re
import os
from bs4 import BeautifulSoup
import urllib2

logs_dir='/home/andy/irclogs/'
html_dir='/var/www/irclinks/'
header="""
<html>
<head>
    <title>{0}</title>
    <link type='text/css' rel='stylesheet' href='styles.css'>
</head>
<body>
    <h1>{0}</h1> {1}
"""

footer="""
<footer>
    created by <a href='http://git.andyblankfield.com/irc_links/blob/master/make_links.py'>irc links</a>
</footer>
</body>
</html>
"""

def get_logs(logs_dir):
    logs = []
    for dirpath, dirname, filename in os.walk(logs_dir):
        for filen in [f for f in filename if f.startswith('#') and f.endswith('.log')]:
            logs.append([filen.lstrip('#')[:-4], os.path.join(dirpath, filen)])
    return logs

def get_title(link):
    try:
        html = urllib2.urlopen(link).read(4096)
        soup = BeautifulSoup(html,"html.parser")
        title = soup.html.head.title.contents[0]
    except Exception as e:
        return "Couldn't get the title :( "
    return title

def get_links(log_file):
    links = []
    link_re = re.compile('http.*:.*[^\s]*')
    nick_re = re.compile('<(.*?)>')
    with open(log_file, 'rb') as f:
        logs = [ line for line in f.readlines() if "-!-" not in line ]
        for line in logs:
            link_match = link_re.search(line)
            if link_match:
                try:
                    nick = nick_re.search(line).groups()[0]
                except Exception as e:
                    nick = "not sure?"
                link = link_match.group().split()[0]
                title = get_title(link).encode('utf-8')
                links.append([nick, link, title])
    return list(reversed(links))

def make_rows(links_data):
    page = "<table><tr><th>Nick</th><th>Link</th><th>Title</th></tr>"
    row = "<tr><td width='20%'>{0}</td>" \
          "<td width='40%'><a href='{1}'>{1}</a></td>" \
          "<td width='40%'>{2}</td></tr>\n"
    for link_data in links_data:
        nick, link, title = link_data
        page += row.format(nick,link,title)
    page += "</table>"
    return page

def make_index():
    logs = get_logs(logs_dir)
    page = header.format("IRC Links", "") + "<ul>\n"
    for log in logs:
        log_name = log[0]
        page += "<li><a href='{0}.html'>{0}</a></li>\n".format(log_name)
    page += "</ul>\n" + footer
    with open(html_dir + "index.html", "w+") as index:
        index.truncate()
        index.write(page)

def make_page_from_logs(logs):
    page = header.format(logs[0].capitalize() + " Links", " - <a href='index.html'>Home</a>\n")
    table = make_rows(get_links(logs[1]))
    html = page + table + footer
    with open(html_dir + logs[0] + ".html", "w+") as page:
        page.truncate()
        page.write(html)

if __name__ == '__main__':
    logs = get_logs(logs_dir)
    for log in logs:
        make_page_from_logs(log)
    make_index()
