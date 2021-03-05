from pythonping import ping
import socket


def check_ping(ip):
    if ping(ip).success():
        return True
    else:
        return False


def check_socket(ip, port):
    sock_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock_stream.connect_ex((ip, port)) == 0:
        sock_stream.close()
        return True
    else:
        sock_stream.close()
        return False
