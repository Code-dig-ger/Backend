from .models import CodechefContest


def create_or_update_codechefContest(contestId):
    # contestId
    contest = CodechefContest.objects.get_or_create(
        contestId = contestId
    )
    # Update contest 
    # Save 