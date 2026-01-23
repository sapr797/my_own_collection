# Коллекция Yandex Cloud ELK v1.0.0

Коллекция Ansible для автоматизации работы с Yandex Cloud и ELK-стеком.

## Содержание коллекции

### Модули
1. **yandex_auth_test** - Проверка аутентификации в Yandex Cloud
   - Проверяет корректность сервисного аккаунта и folder_id
   - Поддерживает validate_only режим

2. **yandex_file_manager** (ранее my_own_module) - Управление файлами
   - Создание, обновление, удаление файлов
   - Гарантированная идемпотентность
   - Управление правами, владельцем, группой

### Роли
1. **yandex_file** - Роль для управления файлами
   - Использует модуль yandex_file_manager
   - Настраиваемые параметры через defaults
   - Подробный вывод результатов

### Плейбуки
1. **use_yandex_file_role.yml** - Пример использования роли
2. **yandex_cloud_integration.yml** - Интеграция с Yandex Cloud

## Быстрый старт

```bash
# Установка коллекции
ansible-galaxy collection install my_own_namespace.yandex_cloud_elk

# Использование модуля аутентификации
- name: Test auth
  my_own_namespace.yandex_cloud_elk.yandex_auth_test:
    service_account_key: '{"id": "test"}'
    folder_id: "b1gtest"

# Использование роли
- hosts: all
  roles:
    - my_own_namespace.yandex_cloud_elk.yandex_file
Требования
Ansible >= 2.9

Python >= 3.6

Доступ к Yandex Cloud (для реального использования)

Лицензия
MIT

Автор
sapr797
