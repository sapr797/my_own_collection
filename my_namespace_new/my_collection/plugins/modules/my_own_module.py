#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Мой собственный модуль для управления файлами
description: |
  Этот модуль создаёт или удаляет файлы с заданным содержимым.
  Пример собственного модуля для демонстрации возможностей Ansible.
version_added: "1.0.0"
author:
  - Ваше Имя (@ваш_github)
options:
  state:
    description:
      - Состояние файла
    type: str
    choices: [ present, absent ]
    default: present
  path:
    description:
      - Путь к файлу
    type: path
    required: true
  content:
    description:
      - Содержимое файла
    type: str
    default: ""
  mode:
    description:
      - Права доступа к файлу (в восьмеричном формате, например 0644)
    type: str
  owner:
    description:
      - Владелец файла
    type: str
  group:
    description:
      - Группа файла
    type: str
requirements:
  - python >= 3.6
notes:
  - Для удаления файла используйте state=absent
  - Для создания файла используйте state=present
'''

EXAMPLES = r'''
# Создать файл с содержимым
- name: Создать тестовый файл
  my_namespace.my_collection.my_own_module:
    path: /tmp/test.txt
    content: "Привет от моего модуля!\nВторая строка."
    mode: "0644"
    owner: "ubuntu"
    state: present

# Удалить файл
- name: Удалить файл
  my_namespace.my_collection.my_own_module:
    path: /tmp/test.txt
    state: absent
'''

RETURN = r'''
path:
  description: Путь к файлу
  type: str
  returned: always
  sample: '/tmp/test.txt'
state:
  description: Состояние файла после выполнения
  type: str
  returned: always
  sample: 'present'
changed:
  description: Были ли внесены изменения
  type: bool
  returned: always
  sample: true
size:
  description: Размер файла в байтах
  type: int
  returned: when state=present
  sample: 42
checksum:
  description: SHA1 контрольная сумма файла
  type: str
  returned: when state=present
  sample: "a1b2c3d4e5f67890123456789012345678901234"
'''

import os
import hashlib
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native

def get_file_checksum(path):
    """Вычисляет SHA1 контрольную сумму файла."""
    try:
        with open(path, 'rb') as f:
            file_hash = hashlib.sha1()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        return None

def main():
    # Определяем параметры модуля
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        path=dict(type='path', required=True),
        content=dict(type='str', default=''),
        mode=dict(type='str'),
        owner=dict(type='str'),
        group=dict(type='str'),
    )

    # Создаём объект модуля
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Получаем параметры
    state = module.params['state']
    path = module.params['path']
    content = module.params['content']
    mode = module.params['mode']
    owner = module.params['owner']
    group = module.params['group']

    result = dict(
        changed=False,
        path=path,
        state=state
    )

    file_exists = os.path.exists(path)

    try:
        if state == 'absent':
            # Удаление файла
            if file_exists:
                if not module.check_mode:
                    os.remove(path)
                result['changed'] = True
                module.exit_json(**result)
            else:
                module.exit_json(**result)

        elif state == 'present':
            # Создание/обновление файла
            if file_exists:
                # Читаем текущее содержимое
                with open(path, 'r') as f:
                    current_content = f.read()
                
                # Проверяем, нужно ли обновлять
                content_changed = current_content != content
                needs_change = content_changed
                
                # Проверяем права доступа
                if mode:
                    current_mode = oct(os.stat(path).st_mode & 0o777)[2:]
                    needs_change = needs_change or (current_mode != mode)
                
                if needs_change:
                    if not module.check_mode:
                        # Обновляем файл
                        with open(path, 'w') as f:
                            f.write(content)
                        
                        # Устанавливаем права доступа
                        if mode:
                            os.chmod(path, int(mode, 8))
                        
                        # Устанавливаем владельца/группу
                        if owner or group:
                            import pwd
                            import grp
                            uid = pwd.getpwnam(owner).pw_uid if owner else -1
                            gid = grp.getgrnam(group).gr_gid if group else -1
                            os.chown(path, uid, gid)
                    
                    result['changed'] = True
                    result['size'] = len(content)
                    result['checksum'] = get_file_checksum(path)
                    module.exit_json(**result)
                else:
                    result['size'] = len(current_content)
                    result['checksum'] = get_file_checksum(path)
                    module.exit_json(**result)
            else:
                # Создаём новый файл
                if not module.check_mode:
                    # Создаём директорию если её нет
                    dir_path = os.path.dirname(path)
                    if dir_path and not os.path.exists(dir_path):
                        os.makedirs(dir_path, exist_ok=True)
                    
                    # Создаём файл
                    with open(path, 'w') as f:
                        f.write(content)
                    
                    # Устанавливаем права доступа
                    if mode:
                        os.chmod(path, int(mode, 8))
                    
                    # Устанавливаем владельца/группу
                    if owner or group:
                        import pwd
                        import grp
                        uid = pwd.getpwnam(owner).pw_uid if owner else -1
                        gid = grp.getgrnam(group).gr_gid if group else -1
                        os.chown(path, uid, gid)
                
                result['changed'] = True
                result['size'] = len(content)
                result['checksum'] = get_file_checksum(path) if not module.check_mode else None
                module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Ошибка: {to_native(e)}", 
                         exception=traceback.format_exc())

if __name__ == '__main__':
    main()
