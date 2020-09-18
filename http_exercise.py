"""
    http 请求 响应示例
"""
from socket import *

sockfd = socket()
sockfd.bind(('0.0.0.0', 8844))
sockfd.listen(5)

while True:

    # 浏览器输入地址后会自动链接服务端
    connfd, addr = sockfd.accept()
    print('Connect from ', addr)
    # 接收到的是来自浏览器的请求
    data = connfd.recv(1024 * 10).decode()
    if not data:  # 产生异常的原因是客户端有时候会断开连接,此时recv会返回一个空,从而出现list index out of range错误
        continue
    print(data)
    num = data.split(' ')[1]
    print(num)

    if num == '/first.html':
        with open('first.html') as f:
            info = f.read()
        # response = """HTTP/1.1 200 OK
        # Content_Type:text/html;charset=UTF-8
        #
        # %s
        # """ % info
        # connfd.send(response.encode())

        # 将数据组织为响应格式:
        response = "HTTP/1.1 200 OK\r\n"  # 响应行
        response += "Content_Type:text/html\r\n"  # 响应头
        response += '\r\n'  # 空行
        response = response.encode() + info.encode()  # 响应体

        # 向浏览器发送内容
        connfd.send(response)
    else:
        response = """HTTP/1.1 404 NOT FOUND
        Content_Type:text/html;charset=UTF-8

        网页丢失了呀
        """
        # 向浏览器发送内容
        connfd.send(response.encode())
    connfd.close()
sockfd.close()
