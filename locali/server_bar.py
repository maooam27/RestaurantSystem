import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 25728))
s.listen(2)

print("Bar Server Started")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    data = conn.recv(1024).decode()
    if data == "Order sent":
        print("Order received")
    conn.close()
