import requests
from bs4 import BeautifulSoup
from time import sleep
import os, json, django
from .models import User
from user.exception import ValidationException


def divisionScraper(contest_id):

    contest_url = f"https://www.codechef.com/api/contests/{contest_id}"
    contest_req = requests.get(contest_url)
    if contest_req.status_code != 200:
        raise ValidationException(
            'Failed Scrapping Codechef Contest Divisions')

    contest_req = contest_req.json()
    return contest_req


def contestScraper(offset, contest_type):

    query_contest_url = f"https://www.codechef.com/api/list/contests/{contest_type}?sort_by=START&sorting_order=desc&offset={offset}&mode=premium"
    # Query URL might change in future.
    contest_data = requests.get(query_contest_url)

    if contest_data.status_code != 200:
        raise ValidationException('Failed Scrapping Codechef Contests')

    contest_data = contest_data.json()

    return contest_data


def problemScraper(contest_code):

    query_problem_url = f"https://www.codechef.com/api/contests/{contest_code}"
    # Query URL might change in future.
    problem_data = requests.get(query_problem_url)
    if problem_data.status_code != 200:
        raise ValidationException('Failed Scrapping Codechef Problems')

    problem_data = problem_data.json()

    return problem_data

def userScraper(user_handle):
    query_user_profile_url = f"https://www.codechef.com/users/{user_handle}"
    r = requests.get(query_user_profile_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    user_details = soup.find('section', class_='user-details')

    name = soup.find('div', class_='user-details-container plr10')
    name = name.find('h1').contents[0]

    country = user_details.find('span', class_='user-country-name').contents[0]

    rating = soup.find('div', class_='rating-header')

    user_rating = soup.find('div', class_='rating-number')
    user_rating = (user_rating.contents)[0]

    user_stars = rating.find('div', class_='rating-star')
    user_stars = len(list(user_stars.find_all('span')))

    user_highest_rating = (rating.find('small').contents)[0]
    user_highest_rating = str(user_highest_rating).split(' ')[-1][:-1]

    ranks = soup.find('div', class_='rating-ranks')
    ranks = ranks.find_all('strong')
    global_rank = ranks[0].contents[0]
    country_rank = ranks[1].contents[0]

    user, isCreated = User.objects.get_or_create(handle=user_handle, username=user_handle)
    user.name = name
    user.stars = user_stars
    user.rating = int(user_rating)
    user.maxRating = int(user_highest_rating)
    user.country = country
    user.country_rank = country_rank
    user.global_rank = global_rank
    user.save()
    
# userScraper("anubhavtyagi")