#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать dns сервер.
Сервер должен принимать соединения по протоколу udp.
Если приходит запрос "domain.name" должен отправлять в ответ ip адрес.
* Доп задание: иметь возможность переопределять записи клиентами:
* ADD my.google.com:228.228.228.228
"""

import socket

def connect_to_udp_dns(hostname, port, buff, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket = (hostname, port)
    print(f"Client is started.\nServer is {server_socket[0]}:{server_socket[1]}\nPress Ctrl-C to exit.\n")
    server_request = ''
    while True:
        try:
            server_request = input("Enter record for request: ")
            if server_request:
                try:
                    sock.sendto(server_request.encode(), server_socket)
                    sock.settimeout(timeout)
                    server_answer, srvfrom = sock.recvfrom(buff)
                    print(f"Server {srvfrom[0]}:{srvfrom[1]} answer:\n{server_answer.decode()}\n")
                except socket.timeout:
                    print(f"Timed out\nIs server {hostname}:{port} running?")
                    sock.close()
                    break
            else:
                continue
        except KeyboardInterrupt:
            sock.close()
            print(f"\nClient exiting ...")
            break

def main():
    connect_to_udp_dns('localhost', 53000, 1024, 2)

if __name__ == "__main__":
    main()
