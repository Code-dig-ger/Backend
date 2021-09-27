# makeResult of a particular contest
from .models import Contest, ContestProblem, ContestParticipation, ContestResult
from problem.models import Problem
from user.models import Profile
from datetime import datetime, timedelta
import requests
import pytz


def get_problemSubmission(participant_handle, prob_id, startTime, endTime):

    problemSubmission = {}
    for prob in prob_id:
        problemSubmission[prob] = None

    res = requests.get("https://codeforces.com/api/user.status?handle=" +
                       participant_handle)
    if res.status_code != 200:
        return problemSubmission
    res = res.json()
    if res['status'] != "OK":
        return problemSubmission

    for submission in res["result"]:
        if 'contestId' in submission['problem'] and 'verdict' in submission:
            problem_id = str(submission["problem"]
                             ['contestId']) + submission["problem"]['index']
            creationTime = submission["creationTimeSeconds"]
            submissionTime = datetime.utcfromtimestamp(creationTime).replace(
                tzinfo=pytz.UTC)

            if submissionTime < startTime:
                break

            if submissionTime >= startTime and submissionTime <= endTime:
                if problem_id in prob_id and submission['passedTestCount'] > 0:
                    if submission['verdict'] == 'OK' and problemSubmission[
                            problem_id] == None:
                        problemSubmission[problem_id] = {
                            'submissionTime': submissionTime - startTime,
                            'penalty': 0
                        }
                    elif problemSubmission[problem_id] != None:
                        problemSubmission[problem_id]['penalty'] += 1

    return problemSubmission


def prepareResult(contest):

    participants = ContestParticipation.objects.filter(contest=contest)
    problems = ContestProblem.objects.filter(contest=contest)
    prob_id = list(problems.values_list('problem__prob_id', flat=True))

    for participant in participants:

        participant_handle = Profile.objects.get(
            owner=participant.user).codeforces
        problemSubmission = get_problemSubmission(
            participant_handle, prob_id, contest.startTime,
            contest.startTime + contest.duration)
        #print(problemSubmission)
        for problem in problems:
            submission = problemSubmission[problem.problem.prob_id]
            if submission != None:
                cr = ContestResult()
                cr.contestParticipation = participant
                cr.contestProblem = problem
                cr.submissionTime = submission['submissionTime']
                cr.penalty = submission['penalty']
                cr.save()

    contest.isResult = True
    contest.save()
    return
