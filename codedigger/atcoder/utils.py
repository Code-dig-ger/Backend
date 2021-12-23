from .api import get_user_results
from .scrapers_utils import get_all_contests_details
from .scrapers import get_user_history


def atcoder_status(handle):
    contests_details = set()
    all_contest = set()
    solved = set()
    wrong = set()

    try:
        res = get_user_history(handle)
    except:
        return (contests_details, all_contest, solved, wrong)

    contests_details = get_all_contests_details(res.content)

    try:
        data = get_user_results(handle)
    except:
        return (contests_details, all_contest, solved, wrong)

    for sub in data:
        all_contest.add(sub["contest_id"])
        if sub["result"] == "AC":
            solved.add(sub["problem_id"])

    for sub in data:
        if sub["result"] != "AC" and sub["problem_id"] not in solved:
            wrong.add(sub["problem_id"])

    return (contests_details, all_contest, solved, wrong)
