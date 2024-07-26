import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 4384))
s.listen(2)

print("Server started")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    data = conn.recv(1024).decode()
    if data == "Order sent":
        print("Order sent")
    conn.close()
