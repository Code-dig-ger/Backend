from .models import contest
from problem.models import Problem
from .api import user_status
from .api_utils import get_prob_id

def CodeforcesAssignProblem(cf_user):

    contests=contest.objects.filter(Type__exact='R')
    contestIds = [ contest.contestId for contest in contests]
    
    Userrating=cf_user['rating']
    Userrating=Userrating // 100 * 100

    # Making a below line that Minimum rating as 1000 and maximum rating as 2500
    if Userrating<=1000:
        Userrating=1000
    if Userrating>=2500:
        Userrating=2500

    # problems -> superset 
    problems=Problem.objects.filter(contest_id__in = contestIds, platform = 'F',difficulty__isnull=False,rating__gte=(Userrating-200),rating__lte=(Userrating+200))


    #taking all the user Submissions that he have done before
    UserSubmissions=user_status(cf_user['handle'])

#  problems2 - >filtered out problems Exculding the problems that user solved
    FilteredProblems=[]
    for problem in problems:
        for submission in UserSubmissions:
            if get_prob_id(submission)!=(problem['prob_id']):
                FilteredProblems.append(problem)
    
    # Assigning the problem as per the order 
    # rating-200,rating-100,=rating,rating+100,rating+200
    AssignedProblem=[]
    Temp_rating=Userrating-200      #Temprary variable for checking the rating
    for i in range(5):
        for problem in FilteredProblems:
            if (problem['rating']//100*100)==Temp_rating:
                AssignedProblem.append(problem)
                break
        Temp_rating+=100

    return AssignedProblem
