import json

from linkedin_api import Linkedin
from linkedin_api.utils.helpers import get_id_from_urn
from utils.helpers import cookies_get_value, cookies_set_value

"""
Поиск компаний

todo написать поиск компаний, людей и вакансий
todo сохранить в бд со связями между собой, модель данных составить 
todo параллельное выполнение этих трех процессов (компании - люди - вакансии)
todo для каждого из процессов
todo прогресс бар возможно вывести 
todo обрабатывать обрыв соединения
"""


def get_company(urn):
    """
    Get company info

    :param urn: LinkedIn URN ID for a company.
    :type urn: int|str
    :return: dict with data
    :rtype: dict
    """
    company = linkedin.get_company(str(urn))
    if company:
        industries = []
        for industry in company['companyIndustries']:
            industries.append(
                {'localized_name': industry['localizedName'], 'entity_urn': get_id_from_urn(industry['entityUrn'])})

        locations = []
        for location in company['confirmedLocations']:
            locations.append(
                {'country': location['country'], 'city': location.get('geographicArea') or location['city']})

        headquarter = {
            'country': company['headquarter']['country'],
            'city': company['headquarter'].get('geographicArea') or company['headquarter']['city']
        }

        data_to_db = {
            'industries': industries,
            'staff_count': company['staffCount'],
            'follower_count': company['followingInfo']['followerCount'],
            'url': company['url'],
            'specialities': company['specialities'],
            'locations': locations,
            'name': company['name'],
            'description': company['description'],
            'urn': get_id_from_urn(company['entityUrn']),
            'headquarter': headquarter,
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
        index = 0
        linkedin.logger.disabled = True
        cookies_subdir = 'search_companies'

        current_progress = cookies_get_value('current_progress', cookies_subdir)

        for index in range(current_progress, limit):
            company = get_company(str(index))
            print(f'viewed: {index}, pull: {limit}')
            cookies_set_value("current_progress", index, cookies_subdir)
            if company:
                print(company)
