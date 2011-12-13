#!/home/henry/weblog/env/bin/python

import sys
from functools import partial
from datetime import date
from os import path, mkdir
from re import escape
from glob import iglob

sys.path.append(path.expanduser('~/weblog'))

import weblog

def output(*args):
    return path.join('./output', *args)

if not path.isdir(output()):
    mkdir(output())
    mkdir(output('weblog'))

copy = partial(weblog.copy, link=True)

def ignore(path):
    for x in ('.', 'output', 'templates', 'robots.txt', 'weblog/doc',
              'weblog/files', 'nginx', 'vanpy/test', 'IDEAS.txt'):
        if path.startswith(x):
            return True
    return False

files = weblog.list_files('.', ignore=ignore)
pages = list(weblog.Page(f, encoding='utf8') for f in files)

TITLE = u'Henry\u2019s Weblog'
URL = 'http://henry.precheur.org/'

posts = list(p for p in pages if hasattr(p, 'date'))
others = list(p for p in pages if p not in posts and not hasattr(p, 'ignore'))

def cmp_page(self, other):
    return cmp(str(self.date), str(other.date))

posts.sort(reverse=True, cmp=cmp_page)

w = weblog.template.Writer('./templates', encoding='utf8')

weblog.publish.feed(output('feed.atom'), posts[:10], URL, TITLE, writer=w)

popular = ('python/copy_list.txt',
           'vim/python.html',
           'python/Dynamically create a type with Python.txt',
           'vim/create_spell_file_for_vim.html',
           'python/rfc3339.html',
           'python/how_to_server_cgi.txt',
           'clan.cx/feedbackarmy.txt',
           'system/ssh-copy-id.txt',
           'system/ipv6.txt',
           'web/http_compression.txt')
weblog.publish.index(output('index.html'), posts,
                     u'{} \u2014 {}'.format(TITLE, posts[0].title),
                     writer=w,
                     popular=popular)

def top_dir(p):
    return path.relpath('.', path.dirname(p.filename)) + '/'

for p in posts:
    o = output(p.output_filename())
    if weblog.newer_than(p.filename, o):
        w.write('post.html.tmpl', o,
                title=p.title, date=p.date, content=p.html(),
                top_dir=top_dir(p))

for p in others:
    o = output(p.output_filename())
    if weblog.newer_than(p.filename, o):
        if o.endswith('/404'):
            t = '/'
        else:
            t = top_dir(p)
        w.write('page.html.tmpl', o, title=p.title, content=p.html(),
                top_dir=t)

copy(pages, output())

copy('images/icons/search.png', output('images', 'icons'))

copy(['favicon.ico', 'robots.txt', 'sitemap.xml'], output())
copy(sorted(iglob('vanpy/test/*')), output('vanpy', 'test'))

f = open(output('redirect.conf'), 'w')

def r(old, new):
    f.write('rewrite "^/%s$" /%s permanent;\n' % (old, new))

for p in posts:
    if p.date > date(2010, 3, 8):
        continue
    dirs = '/'.join((str(p.date.year), str(p.date.month), str(p.date.day)))
    title = p.title.encode('ascii', 'replace')
    old_old_url = escape(dirs + '/' + title + '.html')
    for x in '/\\ ':
        title = title.replace(x, '_')
    old_url = escape(dirs + '/' + title + '.html')
    r(old_url, p.url())
    if p.date.year < 2009 and old_url != old_old_url:
        r(old_old_url, p.url())

r('archives.html', '')
r('archives', '')
r('about.html', 'about')
r('readings.html', 'books')
r('rss.xml', 'feed.atom')
r('python/projects/rfc3339.html', 'projects/rfc3339')
r('vanpyz_test/.*', 'vanpy/test')

f.close()
