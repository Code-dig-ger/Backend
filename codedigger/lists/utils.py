# Models Import
from .models import Solved, ListExtraInfo
from user.models import Profile

# Serializers Import
from .serializers import ProblemSerializer

from .solved_update import codeforces, uva, atcoder, codechef, spoj, atcoder_scraper_check


def update_submissions(qs, user, help_dict):
    # param :
    # qs : Problem QuerySet (List of Problems Object)
    # user: Object of User Model
    # help_dict: Helper Dictionary to check for Codeforces, UVA

    for ele in qs:
        solve = Solved.objects.filter(user=user, problem=ele)
        if not solve.exists():
            if ele.platform == 'F' and help_dict['F']:
                help_dict['F'] = False
                codeforces(user)
            elif ele.platform == 'U' and help_dict['U']:
                help_dict['U'] = False
                uva(user)
            elif ele.platform == 'A':
                atcoder_scraper_check(user, ele)
            elif ele.platform == 'S':
                spoj(user, ele)
            elif ele.platform == 'C':
                codechef(user, ele)
    return help_dict


def getqs(qs, page_size, page):
    qs = qs[page_size * (page - 1):page_size * page]
    return qs


def get_list_platform(user):
    # Param :
    # user : Object of User Model
    user_profile = Profile.objects.get(owner=user)
    temp = ['F']
    if user_profile.spoj != None:
        temp.append('S')
    if user_profile.uva_handle != None:
        temp.append('U')
    if user_profile.atcoder != None:
        temp.append('A')
    if user_profile.codechef != None:
        temp.append('C')
    return temp


def get_total_page(total_problems, page_size):
    # param :
    # total_problems : total number of problems
    # page_size : number of problems in a page
    total_page = total_problems // page_size
    if total_problems % page_size != 0:
        total_page += 1
    return total_page


def get_prev_url(page, url):
    # param :
    # page: current page number
    # path: base url
    if page == 1:
        Prev = None
    else:
        Prev = url + '?page=' + str(page - 1)
    return Prev


def get_next_url(page, url, total_page):
    # param :
    # page: current page number
    # path: base url
    # total_page: total page in list
    if page == total_page:
        Next = None
    else:
        Next = url + '?page=' + str(page + 1)
    return Next


def get_unsolved_page_number(problem_qs, user, page_size):
    # param :
    # problem_qs : 	List of Problems Total
    # user : 		Object of User Model
    # page_size: 	Problem in single page

    total_problems = problem_qs.count()
    total_page = get_total_page(total_problems, page_size)

    page_number = 1
    isCompleted = True
    unsolved_prob = None
    help_dict = {'F': True, 'U': True}
    while page_number <= total_page:
        qs = getqs(problem_qs, page_size, page_number)
        help_dict = update_submissions(qs, user, help_dict)
        for ele in qs:
            solve = Solved.objects.filter(user=user, problem=ele)
            if not solve.exists():
                unsolved_prob = ele.prob_id
                isCompleted = False
                break
        if not isCompleted:
            break
        page_number += 1
    if isCompleted:
        page_number = 1
    return (page_number, unsolved_prob, isCompleted)


def update_page_submission(problem_qs, user, page_size, page_number):
    # param :
    # problem_qs : 	List of Problems Total
    # user : 		Object of User Model
    # page_size: 	Problem in single page
    # page_number: 	Page Number to Update

    qs = getqs(problem_qs, page_size, page_number)
    help_dict = {'F': True, 'U': True}
    update_submissions(qs, user, help_dict)


def get_response_dict(curr_list,
                      user,
                      page_number,
                      page_size,
                      url,
                      problem_qs,
                      isCompleted,
                      unsolved_page=None,
                      unsolved_prob=None):
    # param:
    # curr_list: 	Object of List Model
    # user:			Object of User Model
    # page_number: 	Current Page Number
    # page_size: 	number of problems in a page
    # url:			Base url
    # problem_qs:	List of Problems Total
    # isCompleted: 	is List Completed
    # unsolved_page: First Unsolved Page
    # unsolved_prob: First Unsolved Problem

    total_problems = problem_qs.count()
    total_page = get_total_page(total_problems, page_size)
    qs = getqs(problem_qs, page_size, page_number)

    description = curr_list.description
    name = curr_list.name

    difficulty = None
    video_link = None
    contest_link = None
    editorial = None
    if ListExtraInfo.objects.filter(curr_list=curr_list).exists():
        qs = ListExtraInfo.objects.get(curr_list=curr_list)
        difficulty = qs.difficulty
        video_link = qs.video_link
        contest_link = qs.contest_link
        editorial = qs.editorial

    Prev = get_prev_url(page_number, url)
    Next = get_next_url(page_number, url, total_page)

    res = {
        'status':
        "OK",
        'result':
        ProblemSerializer(qs,
                          many=True,
                          context={
                              "slug": curr_list,
                              "user": user
                          }).data,
        'link': {
            'first': url + "?page=1",
            'last': url + "?page=" + str(total_page),
            'prev': Prev,
            'next': Next,
        },
        'meta': {
            'user': None if user is None else user.username,
            'curr_prob': unsolved_prob,
            'curr_unsolved_page': unsolved_page,
            'completed': isCompleted,
            'name': name,
            'description': description,
            'difficulty': difficulty,
            'video_link': video_link,
            'contest_link': contest_link,
            'editorial': editorial,
            'current_page': page_number,
            'from': (page_number - 1) * page_size + 1,
            'last_page': total_page,
            'path': url,
            'per_page': page_size,
            'to': page_number * page_size,
            'total': total_problems
        }
    }
    return res
