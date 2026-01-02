#!/usr/bin/env python3
import sys
import json

# Добавляем путь к нашему модулю
sys.path.insert(0, 'my_namespace/my_collection/plugins/modules')

# Имитируем аргументы Ansible
sys.argv = ['my_own_module.py', 'path=/tmp/test_direct.txt', 'content=Direct test', 'state=present']

# Запускаем модуль
exec(open('my_namespace/my_collection/plugins/modules/my_own_module.py').read())
