#! /usr/bin/python3

from urllib.error import HTTPError
from cairosvg import svg2pdf
from html.parser import HTMLParser
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO
from urllib import request

test_url = "https://musescore.com/valky/the-champions-ballad-the-legend-of-zelda-breath-of-the-wild"


def get_string(url):
    fp = request.urlopen(url)
    mybytes = fp.read()
    fp.close()
    mystr = mybytes.decode("utf8")
    return mystr


class MyParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        self.svg_urls = []
        super(MyParser, self).__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        try:
            if (tag == 'link') & (attrs.get('type') == 'image/svg+xml'):
                self.svg_urls.append(attrs['href'])
                if attrs['rel'] == 'preload':
                    self.score_url = attrs['href']

        except KeyError:
            return


def parse_html(html):
    parser = MyParser()
    parser.feed(html)
    return parser

# continue from here


def get_pdf_page(url):

    mybytes = svg2pdf(url=url)
    return BytesIO(mybytes)


def gen_pdf(input_streams, output_stream):

    writer = PdfFileWriter()

    for reader in map(PdfFileReader, input_streams):
        writer.addPage(reader.getPage(0))  # all the pdfs are 1 page long
        # since they are generated from separate .svg files
    writer.write(output_stream)
    for f in input_streams:
        f.close()


def main(musescore_url, output_file_name='score.pdf'):
    html = get_string(musescore_url)
    parser = parse_html(html)

    i = 0
    pdf_streams = []

    svg_url = parser.score_url
    while True:
        print(f'trying url: {svg_url}')
        try:
            pdf_stream = get_pdf_page(svg_url)
        except HTTPError:
            break

        pdf_streams.append(pdf_stream)

        svg_url = svg_url.replace(f'/score_{i}.svg', f'/score_{i+1}.svg')
        i += 1

    f = open(output_file_name, 'wb')
    gen_pdf(pdf_streams, f)


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 3:
        print(f'usage: {argv[0]} <url> <file>')
        exit()

    main(argv[1], argv[2])
