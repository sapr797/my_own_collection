# My Ansible Collections Repository

Этот репозиторий содержит различные коллекции Ansible для автоматизации.

## Структура репозитория
my_own_collection/
├── my_own_namespace/
│ └── yandex_cloud_elk/ # Коллекция для Yandex Cloud и ELK
│ ├── galaxy.yml
│ ├── plugins/
│ │ └── modules/
│ │ └── yandex_file_manager.py
│ ├── playbooks/
│ └── roles/
├── ansible_collections/ # Стандартное расположение коллекций
│ └── my_namespace/
│ └── my_collection/
└── README.md

text

## Коллекция my_own_namespace.yandex_cloud_elk

Коллекция для управления ресурсами Yandex Cloud и развертывания ELK-стека.

### Установка

```bash
# Установка из локального архива
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz

# Или сборка из исходников
cd my_own_namespace/yandex_cloud_elk
ansible-galaxy collection build
Использование
Пример использования модуля yandex_file_manager:

yaml
- name: Тестирование модуля
  hosts: localhost
  tasks:
    - name: Создание файла
      my_own_namespace.yandex_cloud_elk.yandex_file_manager:
        path: "/tmp/test.txt"
        state: present
        content: "Тестовое содержимое"
Автор
sapr797 (sapr797@gmail.com)

Лицензия
MIT
