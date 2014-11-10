import urllib2
import json
PORT = 5000

def send_to_suburl(addr, port, suburl, to_send):
    data = json.dumps(to_send)
    url = "http://%s:%d/%s" % (addr, port, suburl)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    f.read()
    f.close()


def send_work(addr, port, to_send):
    send_to_suburl(addr, port, "work", to_send)


def send_result(addr, port, to_send):
    send_to_suburl(addr, port, "presult", to_send)


def join(addr, port):
    send_to_suburl(addr, port, "join", {})
