#!/home/henry/env/weblog/bin/python

from os import path, mkdir
import sys
from datetime import date

sys.path.append(path.expanduser('~/weblog'))

import weblog

if not path.isdir('./output'):
    mkdir('./output')
    mkdir('output/weblog')

# Copy weblog/doc first
weblog.link_tree('weblog/doc', 'output/weblog')

class Page(weblog.Page):
    def output_filename(self):
        if path.basename(self.filename) == 'index.html':
            return self.filename
        else:
            return path.splitext(self.filename)[0]

def ignore(path):
    for x in ('output', 'templates', 'robots.txt', 'weblog/doc', 'nginx'):
        if path.startswith(x):
            return True
    return False

files = weblog.list_files('.', ignore=ignore)
pages = list(Page(f, encoding='utf8') for f in files)

TITLE = u'Henry\u2019s Weblog'
URL = 'http://henry.precheur.org/'

posts = list(p for p in pages if hasattr(p, 'date'))
others = list(p for p in pages if p not in posts)

def cmp_page(self, other):
    return cmp(str(self.date), str(other.date))

posts.sort(reverse=True, cmp=cmp_page)

latest = posts[:10]

w = weblog.template.Writer('./templates', encoding='utf8')

weblog.publish.feed(path.join('output', 'feed.atom'), latest, URL, TITLE,
                    writer=w)
weblog.publish.index(path.join('output', 'index.html'), latest, TITLE,
                     writer=w)

weblog.publish.archives(path.join('output', 'archives'), posts, writer=w)

def top_dir(p):
    return path.relpath('.', path.dirname(p.filename)) + '/'

for p in posts:
    o = path.join('output', p.output_filename())
    if weblog.newer_than(p.filename, o):
        w.write('post.html.tmpl', o,
                title=p.title, date=p.date, content=p.html(),
                top_dir=top_dir(p))

for p in others:
    o = path.join('output', p.output_filename())
    if weblog.newer_than(p.filename, o):
        w.write('page.html.tmpl', o,
                title=p.title, content=p.html(), top_dir=top_dir(p))


weblog.copy_files(pages, 'output')
weblog.copy_files(['common.css', 'archives.css', 'print.css', 'favicon.ico',
                   'robots.txt', 'sitemap.xml'], 'output')

f = open('./output/redirect.conf', 'w')
for p in posts:
    if p.date > date(2009, 4, 1):
        continue
    directories = '/'.join((str(p.date.year), str(p.date.month),
                            str(p.date.day)))
    from re import escape
    title = p.title.encode('ascii', 'replace')
    old_old_url = '^/' + escape(directories + '/' + title + '.html') + '$'
    for x in '/\\ ':
        title = title.replace(x, '_')
    old_url = '^/' + escape(directories + '/' + title + '.html') + '$'
    f.write('rewrite "%s" /%s permanent;\n' % (old_url, p.url()))
    if p.date.year < 2009 and old_url != old_old_url:
        f.write('rewrite "%s" /%s permanent;\n' % (old_old_url, p.url()))

f.write('rewrite "^/archives.html$" /archives permanent;\n')
f.write('rewrite "^/about.html$" /about permanent;\n')
f.write('rewrite "^/readings.html$" /books permanent;\n')
f.write('rewrite "^/rss.xml$" /feed.atom permanent;\n')
f.close()
