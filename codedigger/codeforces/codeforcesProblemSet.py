from problem.models import Problem
from .models import CodeforcesProblemSet

def get_parent(problem):
    try : 
        return CodeforcesProblemSet.objects.get(child = problem).parent
    except : 
        return problem


def check(problem1, problem2):
    return get_parent(problem1).id == get_parent(problem2).id


def join(problem1, problem2):
    if not check(problem1, problem2):
        parent = get_parent(problem1)
        child = get_parent(problem2)
        CodeforcesProblemSet.objects.filter(parent = child).update(parent = parent)
        CodeforcesProblemSet(parent = parent, child = child).save()


def get_similar_problems(problem):
    parent = get_parent(problem)
    childern = list(CodeforcesProblemSet.objects.filter(parent = parent)\
                                .values_list('child', flat = True))
    if not childern:
        return []

    childern.append(parent.id)
    problem_qs = Problem.objects.filter(id__in = childern)\
                                .exclude(id = problem.id)
    return problem_qs
    