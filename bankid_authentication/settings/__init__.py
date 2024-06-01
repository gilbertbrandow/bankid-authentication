import os

def get_secret(secret_id: str, backup=None)->(str | None):
    return os.getenv(secret_id, backup)

if get_secret('PIPELINE') == 'production':
    from .production import *
else: 
    from .local import *