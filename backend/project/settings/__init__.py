import os
from typing import Any

def get_secret(secret_id: str, backup: Any=None)->(str | None):
    return os.getenv(key=secret_id, default=backup)

if get_secret('PIPELINE') == 'production':
    from .production import *
else: 
    from .local import *