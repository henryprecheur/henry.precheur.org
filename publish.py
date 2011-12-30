#!/home/henry/weblog/env/bin/python

import io
import sys
from functools import partial
from os import path, mkdir, makedirs
from argparse import ArgumentParser

from rewrite_url import rewrite_urls

weblog_dev = path.expanduser('~/code/weblog')
if path.isdir(weblog_dev):
    sys.path.insert(0, weblog_dev)

import weblog

copy = partial(weblog.copy, link=True)

def ignore(path):
    for x in ('.', 'output', 'templates', 'robots.txt', 'weblog/doc',
              'weblog/files', 'nginx', 'vanpy/test', 'IDEAS.txt'):
        if path.startswith(x):
            return True
    return False

def publish(output_dir, rewrite):
    def output(*args):
        return path.join(output_dir, *args)

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
        class Writer(weblog.template.Writer):
            def render(self, *args, **kwargs):
                x = super(Writer, self).render(*args, **kwargs)
                return rewrite_url(x)

    else:
        Writer = weblog.template.Writer

    w = Writer('./templates', encoding='utf8')

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
            w.write('post.html.tmpl', output(p.output_filename()),
                    title=p.title, date=p.date, content=p.html(),
                    top_dir=top_dir(p))

    for p in others:
        o = output(p.output_filename())
        if weblog.newer_than(p.filename, o):
            if o.endswith('/404.html'):
                t = '/'
            else:
                t = top_dir(p)
            w.write('page.html.tmpl', o,
                    title=p.title, content=p.html(), top_dir=t)

    copy(pages, output())

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--rewrite', action='store_true')
    parser.add_argument('output_dirs', nargs='+')
    args = parser.parse_args()

    for d in args.output_dirs:
        publish(d, args.rewrite)
