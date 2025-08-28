from dark import DarkMap
# from utils import is_valid_url

def url_exists(url: str, dm:DarkMap) -> bool:
    # print(url, dm.url_db.caller.exist(url))
    return dm.url_db.caller.exist(url)
    