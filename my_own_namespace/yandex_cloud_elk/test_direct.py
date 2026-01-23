#!/usr/bin/env python3
import sys
import json

# Путь к модулю
sys.path.insert(0, '/home/ubuntu/.ansible/collections/ansible_collections/my_own_namespace/yandex_cloud_elk/plugins/modules')
try:
    from yandex_auth_test import main
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Имитируем вызов модуля с параметрами
import tempfile
import os

params = {
    "service_account_key": '{"id": "test-id-123"}',
    "folder_id": "b1gvalidfolder123",
    "validate_only": True
}

# Создаем временный файл с аргументами
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(params, f)
    args_file = f.name

# Заменяем sys.argv, как это делает Ansible
sys.argv = ['yandex_auth_test.py', args_file]

try:
    main()
except SystemExit:
    pass
finally:
    os.unlink(args_file)
