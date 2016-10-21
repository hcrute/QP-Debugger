import socket
import binascii
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 7701
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(10)

values = [1,128]

MESSAGE = bytearray(values)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
MESSAGE[0] = 1
MESSAGE[1] = 0
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

while 1:
	data, addr = sock.recvfrom(4096)
	if bytearray(data)[1] == 1:
		data = bytearray(data)
		string = ""
		for d in data:
			string = string + str(d) + " "
		print string
