#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать класс router.
Должен иметь методы добавить/удалить/вывести список ip address.
Должен иметь методы добавить/удалить/вывести список ip routes.

Есть маршруты к непосредственно-подключенным сетям:
если у устройства есть ip-adress 192.168.5.14/24 на интерфейсе eth1,
значит у него должен быть маршрут:
к сети 192.168.5.0/24 через eth1 или через 192.168.5.14.

Если мы хотим добавить маршрут к какой-нибудь удаленной сети,
то надо проверять доступен ли gateway.

Например мы можем добавить маршрут к 172.16.0.0/16 через gateway
192.168.5.132, только если у нас уже есть маршрут до 192.168.5.132.

Если же мы попытаемся добавить маршрут до какой-либо сети через gateway,
до которого у нас пока еще нет маршрута, то должен вылетать exception.

Например:
Добавляем ip-address 192.168.5.14/24 eth1.
Добавляем маршрут до 172.16.0.0/16 через 192.168.5.1 - ok.
Добавляем маршрут до 172.24.0.0/16 через 192.168.8.1 - exception.
Добавляем маршрут до 172.24.0.0/16 через 172.16.8.1 - ok.

Итого - 1 интерфейс и 3 маршрута в таблице.
"""

from tabulate import tabulate
import ipaddress

class Router:
    """
    A class to represent a router.
    """
    def __init__(self, hostname, number_of_ports):
        self.hostname = hostname
        self.number_of_ports = number_of_ports
        self.interfaces = dict.fromkeys(f"eth{_}" for _ in range(1, number_of_ports + 1))
        self.routes = []
        print(f"Instance {self.hostname} was created with {number_of_ports} ports.\n")

    def __str__(self):
        return f"Hostname: {self.hostname}\nNumber of ports: {self.number_of_ports}.\n"

    def info(self):
        return print(self.__str__())

    def add_ip_address(self, ip_addr, ip_intf):
        ip_addr_str = ipaddress.ip_interface(ip_addr).compressed
        ip_addr_ip_str = ipaddress.ip_interface(ip_addr).ip.compressed
        ip_net_str = ipaddress.ip_interface(ip_addr).network.compressed
        if ip_intf in self.interfaces:
            self.interfaces[ip_intf] = ip_addr_str
            self.routes.append([ip_net_str, ip_addr_ip_str, ip_intf, 'C'])
            return print(f"The address {ip_addr} was added on the interface {ip_intf}.\n")

    def del_ip_address(self, ip_addr, ip_intf):
        ip_addr_str = ipaddress.ip_interface(ip_addr).compressed
        ip_net_str = ipaddress.ip_interface(ip_addr).network.compressed
        if ip_intf in self.interfaces:
            if self.interfaces[ip_intf] == ip_addr:
                for pos, route in enumerate(self.routes):
                    if self.routes[pos][0] == ip_net_str:
                        if self.routes[pos][3] == 'C':
                            del self.routes[pos]
                self.interfaces[ip_intf] = None
                return print(f"The address {ip_addr} was deleted on the interface {ip_intf}.\n")

    def get_ip_address(self):
        headers = ['Interface', 'Address']
        return print(tabulate([(k,v) for k,v in self.interfaces.items()], headers = headers), end='\n\n')

    def add_ip_route(self, ip_net, ip_gw):
        ip_net = ipaddress.ip_network(ip_net)
        ip_net_str = ipaddress.ip_network(ip_net).compressed
        ip_gw = ipaddress.ip_address(ip_gw)
        ip_gw_str = ipaddress.ip_address(ip_gw).compressed
        self_route_intf = [(ipaddress.ip_network(_[0]), _[2]) for _ in self.routes]
        exception = True
        for route_intf in self_route_intf:
            route = route_intf[0]
            intf = route_intf[1]
            if ip_gw in route:
                self.routes.append([ip_net_str, ip_gw_str, intf, 'S'])
                exception = False
        if exception:
            return print(f"No route to gateway {ip_gw}.\n")
        else:
            return print(f"The route to the network {ip_net} throught gateway {ip_gw} via interface {intf} was added.\n")

    def del_ip_route(self, ip_net):
        ip_net_str = ipaddress.ip_network(ip_net).compressed
        self_route_type = [(ipaddress.ip_network(_[0]), _[3]) for _ in self.routes]
        for pos, route in enumerate(self.routes):
            if self.routes[pos][0] == ip_net_str:
                if self.routes[pos][3] == 'S':
                    del self.routes[pos]
                    return print(f"The route to the network {ip_net_str} was deleted.\n")

    def get_ip_route(self):
        headers = ['Network', 'Gateway', 'Interface', 'Type']
        return print(tabulate(self.routes, headers = headers), end='\n\n')

if __name__ == "__main__":
    print(f"# Create class\nr1 = Router('r1', 2)")
    r1 = Router('r1', 2)
    print(f"# Class info\nr1.info()")
    r1.info()
    print(f"# Add address\nr1.add_ip_address('192.168.5.14/24', 'eth1')")
    r1.add_ip_address('192.168.5.14/24', 'eth1')
    print(f"# Add address\nr1.add_ip_address('192.168.1.1/24', 'eth2')")
    r1.add_ip_address('192.168.1.1/24', 'eth2')
    print(f"# Get ip address\nr1.get_ip_address()")
    r1.get_ip_address()
    print(f"# Get ip route\nr1.get_ip_route()")
    r1.get_ip_route()
    print(f"# Delete ip address\nr1.del_ip_address('192.168.1.1/24', 'eth2')")
    r1.del_ip_address('192.168.1.1/24', 'eth2')
    print(f"# Get ip address\nr1.get_ip_address()")
    r1.get_ip_address()
    print(f"# Add ip route\nr1.add_ip_route('172.16.0.0/16', '192.168.5.132')")
    r1.add_ip_route('172.16.0.0/16', '192.168.5.132')
    print(f"# Add ip route\nr1.add_ip_route('172.24.0.0/16', '192.168.8.1')")
    r1.add_ip_route('172.24.0.0/16', '192.168.8.1')
    print(f"# Add ip route\nr1.add_ip_route('172.24.0.0/16', '172.16.8.1')")
    r1.add_ip_route('172.24.0.0/16', '172.16.8.1')
    print(f"# Get ip route\nr1.get_ip_route()")
    r1.get_ip_route()
    # help(Router)
