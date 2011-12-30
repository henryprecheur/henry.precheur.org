import io
import re
import xml.etree
import html5lib

def rewrite_urls(input, output=None):
    doc = html5lib.parse(input,
                         treebuilder='etree',
                         namespaceHTMLElements=False)

    for attr in ('href', 'src', 'data', 'codebase'):
        for x in doc.iterfind('.//*[@{}]'.format(attr)):
            url = x.attrib[attr].strip()

            if url.startswith('http://'):
                continue

            if url.endswith('index.html'):
                u = url[:-len('index.html')]
                x.attrib[attr] = u if u else '/'
            elif url.endswith('.html'):
                x.attrib[attr] = url[:-len('.html')]

    walker = html5lib.treewalkers.getTreeWalker('etree', xml.etree.ElementTree)
    s = html5lib.serializer.HTMLSerializer()

    stream = s.serialize(walker(doc), encoding='utf-8')
    if output:
        # html5lib doesn't serialize the doctype ...
        output.write(u'<!DOCTYPE html>\n')
        for text in stream:
            output.write(text)
    else:
        return u'!<!DOCTYPE html>\n' + u''.join(stream)

__all__ = ('rewrite_urls',)

if __name__ == '__main__':
    # from sys import argv
    from sys import stdin, stdout

    rewrite_urls(stdin, stdout)