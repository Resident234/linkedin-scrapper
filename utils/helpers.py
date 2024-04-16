from datetime import datetime
import requests
from linkedin_api.cookie_repository import CookieRepository


def cookies_wrapper(data, date=datetime.strptime("2050-05-04", "%Y-%m-%d")):
    jar = requests.cookies.RequestsCookieJar()
    jar.set(data['name'], data['value'], expires=date.timestamp())
    jar.set("JSESSIONID", "1234", expires=date.timestamp())
    return jar


def cookies_get_value(name, cookies_subdir):
    repo = CookieRepository(cookies_dir='cookies/' + cookies_subdir + '/')
    cookies = repo.get(name)
    result = 0
    if cookies:
        for cookie in cookies:
            if cookie.name == name and cookie.value:
                result = cookie.value
                break
    return result


def cookies_set_value(name, value, cookies_subdir):
    repo = CookieRepository(cookies_dir='cookies/' + cookies_subdir + '/')
    repo.save(cookies_wrapper({'name': name, 'value': value}), name)
