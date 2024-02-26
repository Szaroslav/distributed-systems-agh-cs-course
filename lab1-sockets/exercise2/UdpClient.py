import socket

server_ip   = "127.0.0.1"
server_port = 9009
msg         = "Python UDP client message (zażółć gęślą jaźń)!"

print("Python UDP client")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(bytes(msg, "utf-8"), (server_ip, server_port))
