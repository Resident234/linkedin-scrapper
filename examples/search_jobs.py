import json

from conf import DEFAULT_PROFILE_PUBLIC_ID, START_PROFILE_PUBLIC_IDS
from linkedin_api import Linkedin

"""
Поиск вакансий в Linkedin
"""

if __name__ == "__main__":
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)

    if credentials:
        limit = 1000
        offset = 0
        linkedin = Linkedin(credentials["username"], credentials["password"], refresh_cookies=False)#TODO если каждый раз куки обновляем, то ловим исключение ChallengeException, но иногда их надо обновлять чтобы не было ошибки что куки в кэше не найдены

        result = linkedin.search_jobs(distance=99999999999, remote='2', location_name='USA', limit=100000)  # offset=offset, keywords='PHP',
        #print(result)
