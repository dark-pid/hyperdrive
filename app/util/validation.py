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

    def check_pid(pid_str):
      regex = r"^(https?://)?(doi\.org/)?([a-zA-Z0-9.-]+)\.([a-z]{2,6})(/[\w\-.]*)*/?$"

      p = re.compile(regex)

      if pid_str is None:
          return False

      if p.match(pid_str):
          return True
      else:
          return False
