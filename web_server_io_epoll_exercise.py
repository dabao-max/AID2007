"""
    基于epoll的web sever
"""
import re
from socket import *
from select import *


class WebServer:
    def __init__(self, host='0.0.0.0', port=8888, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.map = {}
        self.create_sock()
        self.bind_sock()
        self.create_p()

    def create_p(self):
        self.p = epoll()
        self.p.register(self.sock, EPOLLIN)
        self.map[self.sock.fileno()] = self.sock

    def create_sock(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind_sock(self):
        address = (self.host, self.port)
        self.sock.bind(address)

    def start(self):
        self.sock.listen(5)
        print("Listen from port %s" % self.port)
        while True:
            events = self.p.poll()
            for fd, event in events:
                if fd == self.sock.fileno():
                    connfd, addr = self.map[fd].accept()
                    connfd.setblocking(False)
                    print("Connect from:", connfd)
                    self.p.register(connfd, EPOLLIN)
                    self.map[connfd.fileno()] = connfd
                else:
                    self.handler(fd)

    def handler(self, fd):
        request = self.map[fd].recv(1024 * 10).decode()
        print(request)
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)
        if result:
            info = result.group('info')
            print("请求内容:",info)
            self.send(self.map[fd], info)
        else:
            self.p.unregister(self.map[fd])
            self.map[fd].close()
            del self.map[fd]
            return

    def send(self, connfd, info):
        # 组织文件路径
        if info == '/':
            filename = self.html + '/index.html'
        else:
            filename = self.html + info
        try:
            file = open(filename, 'rb')
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry.....</h1>"
            response = response.encode()
        else:
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % (len(data))
            response += "\r\n"
            response = response.encode() + data
        finally:
            # 发送响应给客户端
            connfd.send(response)


if __name__ == '__main__':
    httpd = WebServer(host='0.0.0.0', port=8881, html='./static')
    httpd.start()
