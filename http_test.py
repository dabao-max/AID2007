"""
    http 请求 响应示例
"""
from socket import *

sockfd = socket()
sockfd.bind(('0.0.0.0', 8881))
sockfd.listen(5)

# 浏览器输入地址后会自动链接服务端
connfd, addr = sockfd.accept()
print('Connect from ', addr)

# 接收到的是来自浏览器的请求
data = connfd.recv(1024 * 10)
print(data.decode())
"""GET / HTTP/1.1      # 请求行
Host: 127.0.0.1:8881    # 请求头
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Sec-Fetch-User: ?1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
                            # 空行
                            # 请求体
"""

# # 将数据组织为响应格式:
# response = """HTTP/1.1 200 OK
# Content_Type:text/html;charset=UTF-8
#
# This is a test,你好呀
# """

with open('timg.jpg', 'rb') as f:
    data = f.read()

response = "HTTP/1.1 200 OK\r\n"  # 响应行
response += "Content_Type:image:jpeg\r\n"  # 响应头
response += '\r\n'  # 空行
response = response.encode() + data  # 响应体

# 向浏览器发送内容
connfd.send(response)

connfd.close()
sockfd.close()
