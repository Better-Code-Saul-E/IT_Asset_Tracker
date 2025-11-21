import os

class AppConfig:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    EXPORT_DIR = os.path.join(ROOT_DIR, "exports")

    @classmethod
    def ensure_dirs_exist(cls):
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)