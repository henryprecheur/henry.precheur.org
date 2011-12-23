import io
import xml.etree
import html5lib

def absolute(url):
    '''
    >>> absolute('foo')
    False
    >>> absolute('http://foo')
    True
    >>> absolute('//bar')
    True
    >>> absolute('://bar') # Invalid
    False
    '''
    return bool(re.match(r'(?i)^([a-z]+:)?//', url))

def rewrite_urls(input, output):
    '''
    `input` & `output` are 2 file like objects.
    '''
    doc = html5lib.parse(input,
                         treebuilder='etree',
                         namespaceHTMLElements=False)

    for attr in ('href', 'src', 'data', 'codebase'):
        for x in doc.iterfind('.//*[@{}]'.format(attr)):
            url = x.attrib[attr]

            if absolute(url):
                continue

            if re.search(r'\bindex\.html\s*$', url):
                u = url[:-len('index.html')]
                x.attrib[attr] = u if u else '/'
            elif re.search(r'\b\.html\s*$', url):
                x.attrib[attr] = url[:-len('.html')]

    walker = html5lib.treewalkers.getTreeWalker('etree', xml.etree.ElementTree)
    s = html5lib.serializer.HTMLSerializer()

    # html5lib doesn't serialize the doctype ...
    output.write(u'<!DOCTYPE html>\n')
    for text in s.serialize(walker(doc), encoding='utf-8'):
        output.write(text)

__all__ = ('rewrite_urls',)

if __name__ == '__main__':
    # from sys import argv
    from sys import stdin, stdout

    rewrite_urls(stdin, stdout)
