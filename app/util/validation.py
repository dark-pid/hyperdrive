import re

class ValidationUtil:
    @staticmethod
    def check_url(url_str):
        regex = r"^(https?://)?(www\.)?([a-zA-Z0-9.-]+)\.([a-z]{2,6})(/[\w\-.]*)*/?$"
        p = re.compile(regex)

        if url_str is None:
            return False

        if p.match(url_str):
            return True
        else:
            return False
