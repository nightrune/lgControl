import CGIHTTPServer
import SocketServer

PORT = 80


class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = [""]

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
