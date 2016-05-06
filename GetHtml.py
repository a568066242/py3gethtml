import urllib.request
import urllib.response
import urllib.error
import chardet
import gzip
from io import BytesIO

DETECT_TIME = 5
URLERROR_REPEAT_TIME = 3
USER_AGENT = "lzj"

def getHtmlDefault(url):
    response = getResponse(url)
    page=None
    if(response == None):
        return None
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
        html = page.decode(charset['encoding'],'ignore')
        return html
    else:
        print("can't decode %s" % url)
        return None

def getHtml(url,charset=None):
    if(charset is None):
        return getHtmlDefault(url)
    else:
        response = getResponse(url)
        if(response is None):
            return None
        else:
            if (response.headers.get('Content-Encoding') == 'gzip'):
                # decompress
                page = decompress(response.read())
            else:
                page = response.read()
            return page.decode(charset,'ignore')


def getResponse(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    time = 0
    response = None
    while (time < URLERROR_REPEAT_TIME):
        try:
            response = urllib.request.urlopen(request)
            time = URLERROR_REPEAT_TIME
        except urllib.error.URLError:
            time += 1
    return response


def decompress(compressdate):
    bytes_io = BytesIO(compressdate)
    gzipper = gzip.GzipFile(fileobj=bytes_io)
    return gzipper.read()
