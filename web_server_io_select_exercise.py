"""
    web sever

    完成一个类,提供者
    让他能够使用这个类快速搭建后端服务器内容
"""
from socket import *
from select import select


# 实现具体功能的类
class WebSever:
    def __init__(self, host="0.0.0.0", port=8888, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    # 启动服务
    def start(self):
        self.sock.listen(5)
        print("Listen from :",self.port)
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd, addr = self.sock.accept()
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # r.setblocking(False)
                    data = r.recv(1024 * 10).decode()
                    if not data:
                        self.rlist.remove(r)
                        r.close()
                        continue
                    num = data.split(' ')[1]
                    print(num)
                    try:
                        self.run(num, r)
                    except:
                        continue

    def run(self, num, connfd):
        if num == "/" or num == '/index.html':
            with open('%s/index.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        elif num == '/amusement.html':
            with open('%s/amusement.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        elif num == '/learn.html':
            with open('%s/learn.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        elif num == '/setupwebsite.html':
            with open('%s/setupwebsite.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        elif num == '/shop.html':
            with  open('%s/shop.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        elif num == '/use.html':
            with open('%s/use.html' % self.html, 'rb') as file:
                data = file.read()
            self.response = "HTTP/1.1 200 OK\r\n"
            self.response += "Content-Type:text/html\r\n"
            self.response += "Content-Length:%d\r\n" % (len(data))
            self.response += "\r\n"
            self.response = self.response.encode() + data
            connfd.send(self.response)

        else:
            self.response = """HTTP/1.1 404 NOT FOUND
            Content_Type:text/html;charset=UTF-8

            网页丢失了呀
            """
            connfd.send(self.response.encode())


if __name__ == '__main__':
    # 1.使用者怎么利用这个类
    # 2.实现类的功能需要使用者提供什么(传参)
    #         地址      网页
    httpd = WebSever(host='0.0.0.0', port=8808, html='./static')
    httpd.start()
