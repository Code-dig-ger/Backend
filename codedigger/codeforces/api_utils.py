from user.exception import ValidationException

from .api import user_status


def is_contestant(submission):
    return True if submission['author']['participantType'] == 'CONTESTANT' \
        else False


def is_practice(submission):
    return True if submission['author']['participantType'] == 'PRACTICE' \
        else False


def is_verdict_ok(submission):
    return True if submission['verdict'] == 'OK' else False


def get_prob_id(submission):
    return str(
        submission['problem']['contestId']) + submission['problem']['index']


def get_wrong_submission(submissions,
                         SolvedProblems=set(),
                         UpsolvedProblems=set()):
    Wrong = set()
    for submission in submissions:
        if 'contestId' in submission:
            if 'verdict' in submission:
                # to be sure verdict is present
                prob_id = get_prob_id(submission)
                if not is_verdict_ok(submission) and \
                    prob_id not in SolvedProblems and \
                    prob_id not in UpsolvedProblems:
                    Wrong.add(prob_id)
    return Wrong


def get_correct_submissions(submissions):
    Correct = set()  # Problems Accepted
    for submission in submissions:
        if 'contestId' in submission:
            # to be sure this is a contest problem
            contestId = submission['contestId']
            if 'verdict' in submission:
                # to be sure verdict is present
                if is_verdict_ok(submission):
                    Correct.add(get_prob_id(submission))
    return Correct


def upsolve_status(handle):
    RContest = set()  # Rated Contest
    VContest = set()  # Virtual Contest
    PContest = set()  # Practice Contest

    SolvedInContest = set()  # Problems Solved in Contest
    Upsolved = set()  # Problems Solved after Contest/ Practice
    submissions = user_status(handle=handle)

    for submission in submissions:
        if 'contestId' in submission:
            # to be sure this is a contest problem
            contestId = submission['contestId']

            if is_contestant(submission):
                RContest.add(contestId)
            elif is_practice(submission):
                PContest.add(contestId)
            else:
                VContest.add(contestId)

            if 'verdict' in submission:
                # to be sure verdict is present
                if is_verdict_ok(submission):
                    if not is_practice(submission):
                        SolvedInContest.add(get_prob_id(submission))
                    else:
                        Upsolved.add(get_prob_id(submission))

    Wrong = get_wrong_submission(submission, SolvedInContest, Upsolved)
    return (RContest, VContest, PContest, SolvedInContest, Upsolved, Wrong)


def correct_submissions(handle):
    submissions = user_status(handle=handle)
    return get_correct_submissions(submissions)


def wrong_submissions(handle):
    submissions = user_status(handle=handle)
    Correct = get_correct_submissions(submissions)
    return get_wrong_submission(submissions, Correct)


def multiple_correct_submissions(handles):
    submissions = set()
    for handle in handles:
        submissions |= correct_submissions(handle)
    return submissions
