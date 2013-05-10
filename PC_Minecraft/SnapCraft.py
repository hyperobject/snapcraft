#Snap! extension base by Technoboy10
import SimpleHTTPServer
class CORSHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
	path = self.path
	print path
	ospath = os.path.abspath('')
	if 'command' in path:
		regex = re.compile("\/command(.+)")
		m = regex.match(path)
		server.command(urllib.unquote(m.group(1)))
	elif 'message' in path:
		regex = re.compile("\/message(.+)")
		m = regex.match(path)
		server.message(urllib.unquote(m.group(1)))
	elif path == '/stop':
		server.stop()
	elif path == '/start':
		server.start()
	elif path == '/status':
		f = open(ospath + '/return', 'w+')
		f.write(str(server.status()))
		f.close()
		f = open(ospath + '/return', 'rb')
		ctype = self.guess_type(ospath + '/return')
		self.send_response(200)
	        self.send_header("Content-type", ctype)
	        fs = os.fstat(f.fileno())
	        self.send_header("Content-Length", str(fs[6]))
	        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
	        self.send_header("Access-Control-Allow-Origin", "*")
	        self.end_headers()
	        return f
	elif path == '/players': 
		f = open(ospath + '/return', 'w+')
		f.write(' '.join(server.players()))
		f.close()
		f = open(ospath + '/return', 'rb')
		ctype = self.guess_type(ospath + '/return')
		self.send_response(200)
	        self.send_header("Content-type", ctype)
	        fs = os.fstat(f.fileno())
	        self.send_header("Content-Length", str(fs[6]))
	        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
	        self.send_header("Access-Control-Allow-Origin", "*")
	        self.end_headers()
	        return f
	elif 'console' in path:
		regex = re.compile("\/console([0-9]+)")
		m = regex.match(path)
		f = open(ospath + '/return', 'w+')
		f.write(str(server.console(int(m.group(1)))))
		f.close()
		f = open(ospath + '/return', 'rb')
		ctype = self.guess_type(ospath + '/return')
		self.send_response(200)
	        self.send_header("Content-type", ctype)
	        fs = os.fstat(f.fileno())
	        self.send_header("Content-Length", str(fs[6]))
	        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
	        self.send_header("Access-Control-Allow-Origin", "*")
	        self.end_headers()
	        return f
	elif 'chat' in path:
		regex = re.compile("\/chat([0-9]+)")
		m = regex.match(path)
		f = open(ospath + '/return', 'w+')
		f.write(str(server.chat(int(m.group(1)))))
		f.close()
		f = open(ospath + '/return', 'rb')
		ctype = self.guess_type(ospath + '/return')
		self.send_response(200)
	        self.send_header("Content-type", ctype)
	        fs = os.fstat(f.fileno())
	        self.send_header("Content-Length", str(fs[6]))
	        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
	        self.send_header("Access-Control-Allow-Origin", "*")
	        self.end_headers()
	        return f
		
if __name__ == "__main__":
    import os
    import re
    import SocketServer
    import urllib
    import mc #mc.py
    PORT = 1303 #MC
    server = mc.Server()
    server.start()
    Handler = CORSHTTPRequestHandler
    #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    print "Go ahead and launch Snap!."
    httpd.serve_forever()

