import json
import time

from conf import DEFAULT_PROFILE_PUBLIC_ID, START_PROFILE_PUBLIC_IDS
from linkedin_api import Linkedin
from linkedin_api.utils.helpers import get_id_from_urn
from utils.helpers import cookies_get_value, cookies_set_value

"""
Поиск вакансий в Linkedin
"""


def get_job(urn):
    """
    Get job info

    :param urn: LinkedIn URN ID .
    :type urn: int|str
    :return: dict with data
    :rtype: dict
    """
    job = linkedin.get_job(str(urn))
    if job:
        skills_data = linkedin.get_job_skills(str(urn))
        skill_match_statuses = skills_data.get('skillMatchStatuses')

        data_to_db = {
            'urn': get_id_from_urn(job['dashEntityUrn']),
            'company_urn': get_id_from_urn(job['companyDetails']['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']['company']),
            'company_name': job['companyDetails']['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']['companyResolutionResult']['name'],
            'company_url': job['companyDetails']['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']['companyResolutionResult']['url'],
            'job_state': job['jobState'],
            'description': job['description']['text'],
            'title': job['title'],
            'work_remote_allowed': job['workRemoteAllowed'],
            'location': job['formattedLocation'],
            'skills': list([skill['skill']['name'] for skill in skills_data['skillMatchStatuses']]) if skill_match_statuses else []
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
        linkedin.logger.disabled = True
        repeat_count = 0
        cookies_subdir = 'search_jobs'

        current_progress = cookies_get_value('current_progress', cookies_subdir)

        job = get_job('3894460323')

        for index in range(current_progress, limit):
            job = get_job(str(index))
            print(f'viewed: {index}, pull: {limit}')
            cookies_set_value("current_progress", index, cookies_subdir)
            if job:
                print(job)
