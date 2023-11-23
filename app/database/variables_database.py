import os


class ConfigVariables:

    def __init__(self):
        os.environ.setdefault("DB_HOST", "127.0.0.1")
        os.environ.setdefault("DB_PORT", "5432")
        os.environ.setdefault("DB_PASS", "postgres")
        os.environ.setdefault("DB_USER", "postgres")
        os.environ.setdefault("DB_NAME", "hyperdrive")

    def get_db_host(self):
        return os.environ["DB_HOST"]

    def set_db_host(self, value):
        os.environ["DB_HOST"] = value

    def get_db_port(self):
        return os.environ["DB_PORT"]

    def set_db_port(self, value):
        os.environ["DB_PORT"] = value

    def get_db_pass(self):
        return os.environ["DB_PASS"]

    def set_db_pass(self, value):
        os.environ["DB_PASS"] = value

    def get_db_user(self):
        return os.environ["DB_USER"]

    def set_db_user(self, value):
        os.environ["DB_USER"] = value

    def get_db_name(self):
        return os.environ["DB_NAME"]

    def set_db_name(self, value):
        os.environ["DB_NAME"] = value
