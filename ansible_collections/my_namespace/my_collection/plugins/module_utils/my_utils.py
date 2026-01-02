#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import hashlib

def calculate_checksum(data):
    """Вычисляет SHA256 контрольную сумму строки."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def validate_path(path):
    """Проверяет валидность пути."""
    import os
    if os.path.isabs(path):
        return True
    return False

class FileManager:
    """Класс для управления файлами."""
    
    def __init__(self, path):
        self.path = path
    
    def exists(self):
        import os
        return os.path.exists(self.path)
    
    def get_size(self):
        import os
        if self.exists():
            return os.path.getsize(self.path)
        return 0
