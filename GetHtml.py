import urllib.request
import urllib.response
import chardet
import gzip
from io import BytesIO

DETECT_TIME = 5
USER_AGENT = "lzj"

def getHtml(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    response = urllib.request.urlopen(request)
    page=None
    if(response.headers.get('Content-Encoding') == 'gzip'):
        #decompress
        page = decompress(response.read())
    else:
        page = response.read()
    charset = chardet.detect(page)
    time = 0

    while (charset['encoding'] == None and time < DETECT_TIME):
        charset = chardet.detect(page)
        ++time

    if (charset['encoding'] != None):
        html = page.decode(charset['encoding'])
        return html
    else:
        print("can't decode %s" % url)
        return None


def decompress(compressdate):
    bytes_io = BytesIO(compressdate)
    gzipper = gzip.GzipFile(fileobj=bytes_io)
    return gzipper.read()

