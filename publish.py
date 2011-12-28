#!/home/henry/weblog/env/bin/python

import io
import sys
from functools import partial
from datetime import date
from os import path, mkdir, makedirs
from re import escape
from glob import iglob

from rewrite_url import rewrite_urls

sys.path.append(path.expanduser('~/code/weblog'))

import weblog

def output(*args):
    return path.join('./output', *args)

copy = partial(weblog.copy, link=True)

def ignore(path):
    for x in ('.', 'output', 'templates', 'robots.txt', 'weblog/doc',
              'weblog/files', 'nginx', 'vanpy/test', 'IDEAS.txt'):
        if path.startswith(x):
            return True
    return False

def publish(rewrite):
    files = weblog.list_files('.', ignore=ignore)
    pages = list(weblog.Page(f, encoding='utf8') for f in files)

    TITLE = u'Henry\u2019s Weblog'
    URL = 'http://henry.precheur.org/'

    posts = list(p for p in pages if hasattr(p, 'date'))
    others = list(p for p in pages if p not in posts and not hasattr(p, 'ignore'))

    def cmp_page(self, other):
        return cmp(str(self.date), str(other.date))

    posts.sort(reverse=True, cmp=cmp_page)

    if rewrite:
        class OutputFile(object):
            def __init__(self, filename):
                self.name = output(filename)

                # Create directory if it doesn't exist
                d = path.dirname(self.name)
                if not path.isdir(d):
                    makedirs(d)

                self._file = io.FileIO(self.name, 'w')

            def write(self, text):
                rewrite_urls(io.StringIO(text), self._file)
    else:
        OutputFile = lambda x: io.FileIO(output(x), 'w')

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
    weblog.publish.index(OutputFile('index.html'), posts,
                         u'{} \u2014 {}'.format(TITLE, posts[0].title),
                         writer=w,
                         popular=popular)

    def top_dir(p):
        return path.relpath('.', path.dirname(p.filename)) + '/'

    for p in posts:
        o = output(p.output_filename())
        if weblog.newer_than(p.filename, o):
            w.write('post.html.tmpl', OutputFile(p.output_filename()),
                    title=p.title, date=p.date, content=p.html(),
                    top_dir=top_dir(p))

    for p in others:
        o = output(p.output_filename())
        if weblog.newer_than(p.filename, o):
            if o.endswith('/404.html'):
                t = '/'
            else:
                t = top_dir(p)
            w.write('page.html.tmpl', OutputFile(p.output_filename()),
                    title=p.title, content=p.html(), top_dir=t)

    copy(pages, output())

if __name__ == '__main__':
    publish('rewrite' in sys.argv)
