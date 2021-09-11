#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Напишите программу, которая читает данные из файлов
/etc/passwd и /etc/group на вашей системе и выводит
следующую информацию в файл output.txt:
1. Количество пользователей, использующих все имеющиеся
интерпретаторы-оболочки.
( /bin/bash - 8 ; /bin/false - 11 ; ... )
2. Для всех групп в системе - UIDы пользователей
состоящих в этих группах.
( root:1, sudo:1001,1002,1003, ...)
"""

shell_list = []
user_list = {}
with open('passwd', 'r') as file_passwd:
    for line in file_passwd:
        p_uname = line.split(":")[0]
        p_uid = line.split(":")[2]
        p_gid = line.split(":")[3]
        p_shell = line.split(":")[6].strip()
        user_list[p_uname] = {'uid': p_uid, 'gid': p_gid}
        shell_list.append(p_shell)
shell_freq = {shell: shell_list.count(shell) for shell in shell_list}
shell_str = ' ; '.join(shell + ' - ' + str(freq) for shell, freq in shell_freq.items())

group_list = {}
with open('group', 'r') as file_group:
    for line in file_group:
        g_gname = line.split(":")[0].strip()
        g_gid = line.split(":")[2].strip()
        g_members = line.split(":")[3].strip().split(",")
        group_list[g_gname] = {'gid': g_gid, 'members': [user_list[member]['uid'] for member in g_members if member]}
for user, uprop in user_list.items():
    for group, gprop in group_list.items():
        if uprop['gid'] == gprop['gid']:
            group_list[group]['members'].append(uprop['uid'])
group_str = ', '.join([f"{group}:{','.join(gids['members'])}" for group, gids in group_list.items()])

with open('output.txt', 'w') as file_output:
    file_output.write(shell_str + '\n')
    file_output.write(group_str + '\n')
    file_output.flush()
    print(f"Записано {file_output.tell()} bytes в файл {file_output.name}")
    file_output.close()
