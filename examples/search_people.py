import json
import time

from linkedin_api import Linkedin
from utils.helpers import cookies_get_value, cookies_set_value

"""
Поиск всех пользователей в Linkedin
todo троттлинг для поисковых выборок
"""

if __name__ == "__main__":
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)

    if credentials:
        linkedin = Linkedin(credentials["username"], credentials["password"])
        limit = 5000
        step = 10
        repeat_count = 0
        cookies_subdir = 'search_people'

        offset = cookies_get_value('current_progress', cookies_subdir)

        while True:
            peoples = linkedin.search_people(offset=offset, limit=step)
            if not len(peoples) or offset >= limit:
                print(f'sleep for {20} sec')
                time.sleep(20)
                if repeat_count >= 10:
                    break
            print(offset, peoples)  # , len(peoples)
            cookies_set_value("current_progress", offset, cookies_subdir)
            offset += len(peoples)
            repeat_count = 0
