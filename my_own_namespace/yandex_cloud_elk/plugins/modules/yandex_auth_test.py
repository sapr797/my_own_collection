#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yandex_auth_test
short_description: Тест аутентификации в Yandex Cloud
description:
  - Модуль для проверки корректности аутентификационных данных Yandex Cloud
  - Проверяет наличие обязательных параметров для работы с API Yandex Cloud
version_added: "1.0.0"
author:
  - Ваше Имя (@sapr797)
requirements:
  - python >= 3.6
options:
  service_account_key:
    description:
      - JSON-ключ сервисного аккаунта Yandex Cloud или строка с JSON
      - Может быть строкой, словарём или JSON-строкой с экранированием
    required: true
    type: raw
    no_log: true
  folder_id:
    description:
      - Идентификатор каталога Yandex Cloud
    required: true
    type: str
  validate_only:
    description:
      - Режим только проверки (без реальных вызовов API)
    required: false
    type: bool
    default: true
notes:
  - В режиме validate_only=True модуль только проверяет формат данных
seealso:
  - name: Yandex Cloud Documentation
    description: Официальная документация Yandex Cloud
    link: https://cloud.yandex.ru/docs
'''

EXAMPLES = r'''
# Пример 1: Передача JSON как строки
- name: Test with JSON string
  my_own_namespace.yandex_cloud_elk.yandex_auth_test:
    service_account_key: '{"id": "test-id", "key": "value"}'
    folder_id: "b1gtest123"
    validate_only: true

# Пример 2: Передача словаря
- name: Test with dictionary
  my_own_namespace.yandex_cloud_elk.yandex_auth_test:
    service_account_key:
      id: "test-id"
      service_account_id: "test-sa"
    folder_id: "cat456"

# Пример 3: Невалидный JSON (ожидается ошибка)
- name: Test with invalid JSON
  my_own_namespace.yandex_cloud_elk.yandex_auth_test:
    service_account_key: "not-a-json"
    folder_id: "b1gtest456"
  ignore_errors: true
'''

RETURN = r'''
authenticated:
  description: Результат проверки аутентификации
  returned: always
  type: bool
folder_id:
  description: Идентификатор каталога
  returned: always
  type: str
message:
  description: Сообщение о результате
  returned: always
  type: str
validation_passed:
  description: Прошла ли валидация формата
  returned: always
  type: bool
service_account_id:
  description: Идентификатор сервисного аккаунта
  returned: when success
  type: str
'''

import json
import traceback
from ansible.module_utils.basic import AnsibleModule

def decode_json_data(data, module):
    """Умное декодирование JSON-данных из разных форматов"""
    # Если это уже словарь - возвращаем как есть
    if isinstance(data, dict):
        return data
    
    # Если это строка
    if isinstance(data, str):
        # Пробуем убрать возможные экранирующие слэши
        cleaned_data = data.replace('\\"', '"').replace("\\'", "'")
        
        # Пробуем декодировать JSON
        try:
            return json.loads(cleaned_data)
        except json.JSONDecodeError:
            # Если не удалось, пробуем убрать лишние кавычки
            if cleaned_data.startswith('"') and cleaned_data.endswith('"'):
                cleaned_data = cleaned_data[1:-1]
                try:
                    return json.loads(cleaned_data)
                except json.JSONDecodeError:
                    # Если все попытки не удались, возвращаем None
                    return None
    
    # Если это не строка и не словарь
    return None

def main():
    module_args = dict(
        service_account_key=dict(type='raw', required=True, no_log=True),
        folder_id=dict(type='str', required=True),
        validate_only=dict(type='bool', default=True),
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    service_account_key = module.params['service_account_key']
    folder_id = module.params['folder_id']
    validate_only = module.params['validate_only']
    
    result = dict(
        changed=False,
        authenticated=False,
        folder_id=folder_id,
        message='',
        validation_passed=False,
        service_account_id=None
    )
    
    try:
        # Декодируем данные сервисного аккаунта
        key_data = decode_json_data(service_account_key, module)
        
        if key_data is None:
            # Не удалось декодировать JSON
            result['message'] = 'Service account key is not valid JSON'
            result['validation_passed'] = False
            result['authenticated'] = False
            module.exit_json(**result)
            return
        
        result['validation_passed'] = True
        
        # Извлекаем ID сервисного аккаунта
        if isinstance(key_data, dict):
            if 'service_account_id' in key_data:
                result['service_account_id'] = key_data['service_account_id']
            elif 'id' in key_data:
                result['service_account_id'] = key_data['id']
        
        # Проверяем формат folder_id
        if folder_id and folder_id.startswith(('b1g', 'cat', 'aje')):
            result['authenticated'] = True
            result['message'] = f'Validation passed for folder: {folder_id}'
        else:
            result['message'] = f'Invalid folder ID format: {folder_id}'
            
        module.exit_json(**result)
        
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        module.fail_json(msg=error_msg, exception=traceback.format_exc())

if __name__ == '__main__':
    main()
