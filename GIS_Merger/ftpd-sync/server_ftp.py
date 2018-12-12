from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import sys

ftp_dir = "./"
addr = "0.0.0.0"

if len(sys.argv)>=3:
    addr = sys.argv[1]
    ftp_dir = sys.argv[2]

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", ftp_dir, perm="elradfmw")
authorizer.add_anonymous(ftp_dir, perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((addr, 8021), handler)
server.serve_forever()