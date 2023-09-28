import os


class ConfigManager:
    EXTERNAL_PID_PARAMETER = "external_pid"
    EXTERNAL_URL_PARAMETER = "external_url"

    def __init__(self):
        os.environ.setdefault("HYPERDRIVE_EXTERNAL_PID_VALIDATION", "NONE")
        os.environ.setdefault("HYPERDRIVE_URL_VALIDATION", "NONE")
        os.environ.setdefault("HYPERDRIVE_PAYLOAD_VALIDATION", "NONE")
        os.environ.setdefault("HYPERDRIVE_OPERATION_MODE", "ASYNC")

    def get_external_pid_validation(self):
        return os.environ["HYPERDRIVE_EXTERNAL_PID_VALIDATION"]

    def set_external_pid_validation(self, value):
        os.environ["HYPERDRIVE_EXTERNAL_PID_VALIDATION"] = value

    def get_url_validation(self):
        return os.environ["HYPERDRIVE_URL_VALIDATION"]

    def set_url_validation(self, value):
        os.environ["HYPERDRIVE_URL_VALIDATION"] = value

    def get_payload_validation(self):
        return os.environ["HYPERDRIVE_PAYLOAD_VALIDATION"]

    def set_payload_validation(self, value):
        os.environ["HYPERDRIVE_PAYLOAD_VALIDATION"] = value

    def get_operation_mode(self):
        return os.environ["HYPERDRIVE_OPERATION_MODE"]

    def set_operation_mode(self, value):
        os.environ["HYPERDRIVE_OPERATION_MODE"] = value
