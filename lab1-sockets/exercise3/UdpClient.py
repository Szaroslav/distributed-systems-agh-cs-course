import socket

server_ip   = "127.0.0.1"
server_port = 9009
msg         = 300

print("Python UDP client")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(msg.to_bytes(4, byteorder="little"), (server_ip, server_port))

msg = int.from_bytes(client.recv(1024), byteorder="little")
print(f"Received message: {msg}")
