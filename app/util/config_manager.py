import os

class ConfigManager:
    EXTERNAL_PID_PARAMETER = 'external_pid'
    EXTERNAL_URL_PARAMETER = 'external_url'

    def __init__(self):
        # Configuração padrão para variáveis de ambiente, se não definidas
        os.environ.setdefault('HYPERDRIVE_EXTERNAL_PID_VALIDATION', 'BASIC')
        os.environ.setdefault('HYPERDRIVE_URL_VALIDATION', 'BASIC')
        os.environ.setdefault('HYPERDRIVE_PAYLOAD_VALIDATION', 'BASIC')

    def get_external_pid_validation(self):
        return os.environ['HYPERDRIVE_EXTERNAL_PID_VALIDATION']

    def set_external_pid_validation(self, value):
        os.environ['HYPERDRIVE_EXTERNAL_PID_VALIDATION'] = value

    def get_url_validation(self):
        return os.environ['HYPERDRIVE_URL_VALIDATION']

    def set_url_validation(self, value):
        os.environ['HYPERDRIVE_URL_VALIDATION'] = value

    def get_payload_validation(self):
        return os.environ['HYPERDRIVE_PAYLOAD_VALIDATION']

    def set_payload_validation(self, value):
        os.environ['HYPERDRIVE_PAYLOAD_VALIDATION'] = value