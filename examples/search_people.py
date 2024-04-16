import json
from itertools import chain, product

from linkedin_api import Linkedin
from linkedin_api.utils.helpers import get_id_from_urn
from utils.helpers import cookies_get_value

"""
Поиск всех пользователей в Linkedin
todo троттлинг для поисковых выборок
todo при поиске пользователей есть ограничение в 1000 элементов, создать ишью в репе по этому вопросу
"""


def get_profile(urn):
    """
    Get people info

    :param urn: LinkedIn URN ID .
    :type urn: int|str
    :return: dict with data
    :rtype: dict
    """
    profile = linkedin.get_profile(str(urn))
    if profile:
        certifications = []
        for certificate in profile['certifications']:
            certifications.append({
                'authority': certificate['authority'],
                'name': certificate['name'],
                'company_urn': get_id_from_urn(certificate['company']['objectUrn']) if certificate.get('company') else '',
                'url': certificate['url'] if certificate.get('url') else '',
            })

        skills = []
        for skill in profile['skills']:
            skills.append(skill['name'])

        experience = []
        for item in profile['experience']:
            experience.append({
                'location_name': item.get('locationName'),
                'company_name': item['companyName'],
                'description': item.get('description'),
                'company_industries': item['industries'] if item.get('industries') else [],
                'title': item['title'],
                'company_urn': get_id_from_urn(item['companyUrn']) if item.get('companyUrn') else '',
            })
        data_to_db = {
            'summary': profile['summary'],
            'industry_name': profile['industryName'],
            'public_id': profile['public_id'],
            'member_urn': get_id_from_urn(profile['member_urn']),
            'name': " ".join([profile['firstName'], profile['lastName']]),
            'location_name': profile['locationName'],
            'geo_country_name': profile['geoCountryName'],
            'geo_country_urn': profile['geoCountryUrn'],
            'industry_urn': get_id_from_urn(profile['industryUrn']),
            'geo_location_urn': get_id_from_urn(profile['geoLocation']['geoUrn']),
            'geo_location_name': profile['geoLocationName'],
            'country_code': profile['location']['basicLocation']['countryCode'],
            'headline': profile['headline'],
            'display_picture_url': profile['displayPictureUrl'],
            'img_100_100': profile.get('img_100_100'),
            'img_200_200': profile.get('img_200_200'),
            'img_400_400': profile.get('img_400_400'),
            'img_800_800': profile.get('img_800_800'),
            'certifications': certifications,
            'projects': [],#todo
            'experience': experience,
            'skills': skills,
        }
        return data_to_db
    else:
        return None


if __name__ == "__main__":
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)

    if credentials:
        linkedin = Linkedin(credentials["username"], credentials["password"])
        limit = 5000
        step = 10
        repeat_count = 0
        linkedin.logger.disabled = True
        cookies_subdir = 'search_people'

        charset = 'abcdefghijklmnopqrstuvwxyz'
        maxlength = 10
        for candidate in chain.from_iterable(product(charset, repeat=i) for i in range(1, maxlength + 1)):
            profile = get_profile(''.join(candidate))
            if profile:
                print(profile)
