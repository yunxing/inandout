from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
import urlparse


def marshall_result(result):
    """
    Turn a result into a string
    """
    return "\n".join(result)


def unmarshall_result(result):
    """
    Turn a string into a result object
    """
    return set(result.split("\n"))


def marshall_info(info):
    return info


def unmarshall_info(info):
    return info


def status_filter(r, info):
    return True


def combine(result1, result2):
    return result1 | result2


def identity_result():
    return set([])


def init_info():
    return "0"


def do_work(request, info):
    soup = bs(urlopen(request))
    # map
    hrefs = [a["href"] for a in soup.findAll("a")]

    # add prefix
    def add_prefix(url):
        if url.startswith("/"):
            return urlparse.urljoin(request, url)
        return url

    images = [image["src"]for image in soup.findAll("img")]
    images = [add_prefix(image) for image in images]
    if info == "1":
        return (set(images), [])
    hrefs = [add_prefix(url) for url in hrefs]
    hrefs = [(url, "1") for url in hrefs]
    return (set(images), set(hrefs))
