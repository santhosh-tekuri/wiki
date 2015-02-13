#!/usr/bin/python
import SimpleHTTPServer, SocketServer

with open ("markdown/md.html", "r") as myfile:
    template = myfile.read()

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path;
        if(path == "/"):
            path = "/index.md";
        if path.endswith(".md"):
            with open (path[1:], "r") as myfile:
                self.wfile.write(template % (myfile.read().replace("<", "&lt;")))
            return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

handler = MyHandler
server = SocketServer.TCPServer(("",8080), handler)
print "open http://localhost:8080 in browser"
server.serve_forever()
