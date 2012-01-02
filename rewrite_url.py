import io
import re
try:
    from elementtree import ElementTree
except ImportError:
    from xml.etree import ElementTree
import html5lib

def rewrite_urls(input, output=None):
    treebuilder = html5lib.treebuilders.getTreeBuilder('etree',
                                                       ElementTree)
    parser = html5lib.HTMLParser(tree=treebuilder, namespaceHTMLElements=False)
    doc = parser.parse(input, encoding='UTF8')

    for tag in doc.getiterator():
        for a in ('href', 'src', 'data', 'codebase'):
            if a not in tag.attrib:
                continue

            url = tag.attrib[a]

            if url.startswith('http://'):
                continue

            if url.endswith('/index.html'):
                u = url[:-len('index.html')]
                tag.attrib[a] = u if u else u'/'
            elif url.endswith('.html'):
                tag.attrib[a] = url[:-len('.html')]

    walker = html5lib.treewalkers.getTreeWalker('etree', ElementTree)
    s = html5lib.serializer.HTMLSerializer()

    stream = s.serialize(walker(doc), encoding='utf-8')
    if output:
        # html5lib doesn't serialize the doctype ...
        output.write(u'<!DOCTYPE html>\n')
        for text in stream:
            output.write(text)
    else:
        return (u'<!DOCTYPE html>\n' +
                u''.join(unicode(x, encoding='utf8') for x in stream))

__all__ = ('rewrite_urls',)

if __name__ == '__main__':
    # from sys import argv
    from sys import stdin, stdout

    rewrite_urls(stdin, stdout)
