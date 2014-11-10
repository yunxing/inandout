import socket
import master
import slave
import transport
from flask import Flask

app = Flask(__name__)
app.debug = True
# There is already a master, run as slave
slave.decorate(app, transport.PORT)
try:
    ip = socket.gethostbyname('master') # result from hosts file
    join(ip, transport.PORT)
except socket.error:
    # Coudldn't find master node, run as master
    master.decorate(app)
