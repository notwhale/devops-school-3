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
import json
import ipaddress

def json_load(filename):
    """
    Read JSON file and return dict.
    """
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        print(f"File {filename} not found.\nEmpty database loaded.\n")
    return data

def json_save(filename, data):
    """
    Save dict to JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def run_udp_dns(hostname, port, buff, dnsdb):
    """
    UDP DNS Server which can reply to requests and modify its own database.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket = (hostname, port)
    print(f"UDP server is running on {server_socket[0]} port {server_socket[1]}\nPress Ctrl-C to stop.\n")
    sock.bind((server_socket))
    dns_records = json_load(dnsdb)
    while True:
        try:
            client_request, client_address = sock.recvfrom(buff)
            print(f"Received {len(client_request)} bytes from {client_address}")
            if client_request:
                client_request = client_request.decode()
                client_request_list = client_request.strip().split()
                if len(client_request_list) > 1:
                    dns_commnad, dns_record, *dns_rest = client_request_list
                    if dns_commnad == 'ADD' and all((dns_commnad, dns_record, dns_rest)):
                        dns_addresses = []
                        for ip in dns_rest:
                            try:
                                dns_addresses.append(ipaddress.ip_address(ip).compressed)
                            except:
                                answ = f"Wrong ip address: {ip}"
                        if dns_addresses:
                            dns_records[dns_record] = dns_addresses
                            answ = f"Record {dns_record} {', '.join(dns_records[dns_record])} has been added."
                    elif dns_commnad == 'DEL' and all((dns_commnad, dns_record)):
                        if dns_records.get(dns_record):
                            del dns_records[dns_record]
                            answ = f"Record {dns_record} has been deleted."
                        else:
                            answ = f"Record {dns_record} not in database."
                    else:
                        answ = f"Wrong command: {client_request}"
                else:
                    if dns_records.get(client_request):
                        answ = f"{client_request}:\n" + '\n'.join(dns_records[client_request])
                    else:
                        answ = f"{client_request} not found."
            else:
                answ = f"Empty request!"
            sent = sock.sendto(answ.encode(), client_address)
            print(f"Sent {sent} bytes to {client_address}")
        except KeyboardInterrupt:
            print(f"\nSaving database {dnsdb} ...")
            json_save(dnsdb, dns_records)
            print(f"Server stopping ...")
            break

def main():
    """
    Run server
    """
    run_udp_dns('localhost', 53000, 1024, 'dns.json')

if __name__ == "__main__":
    main()
