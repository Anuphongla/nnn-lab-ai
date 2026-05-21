from html.parser import HTMLParser
import sys

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        data = data.strip()
        if data:
            self.text += data + "\n"

with open('gitbook.html', 'r', encoding='utf-8') as f:
    html = f.read()

parser = HTMLFilter()
parser.feed(html)

with open('gitbook.txt', 'w', encoding='utf-8') as f:
    f.write(parser.text)
