#Snap! extension base by Technoboy10
import SimpleHTTPServer
class CORSHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
	path = self.path
	print path
	ospath = os.path.abspath('')
	if 'setblock' in path:
		regex = re.compile("\/setblock([0-9|-]+),([0-9|-]+),([0-9|-]+),([0-9|-]+),([0-9|-]+)")
		m = regex.match(path)
		mc.setBlock(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
	elif 'chat' in path:
		regex = re.compile("\/chat([0-9a-zA-Z|\!|\?])")
		m = regex.match(path)
		mc.postToChat(m.group(1))
	elif 'moveplayer' in path:
		regex = re.compile("\/moveplayer([0-9|-]+),([0-9|-]+),([0-9|-]+)")
		m = regex.match(path)
		mc.player.setPos(m.group(1), m.group(2), m.group(3))
	elif "getblock" in path: #return data
		regex = re.compile("\/getblock([0-9|-]+),([0-9|-]+),([0-9|-]+)")
		m = regex.match(path)
		f = open(ospath + '/return', 'w+')
		f.write(str(mc.getBlock(m.group(1), m.group(2), m.group(3))))
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
	elif 'getplayer' in path:
		regex = re.compile("\/getplayer([x|y|z])")
		m = regex.match(path)
		pos = mc.player.getTilePos()
		if m.group(1) == 'x':
			value = pos.x
		elif m.group(1) == 'y':
			value = pos.y
		elif m.group(1) == 'z':
			value = pos.z
		f = open(ospath + '/return', 'w+')
		f.write(str(value))
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
    import minecraft
    PORT = 1303 #(M)ine(C)raft
    mc = minecraft.Minecraft.create()
    Handler = CORSHTTPRequestHandler
    #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    print "Go ahead and launch Snap!."
    httpd.serve_forever()

