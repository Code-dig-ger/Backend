from .scraper import problem_page

def problem_page_text(url):
    soup = problem_page(url)
    return soup.find_all('div', {'class': 'problem-statement'})[0]\
                .find_all('div', {'class' : ''})[0].text

def isSameProblem(url1, url2):
    text1 = problem_page_text(url1)
    text2 = problem_page_text(url2)

    return text1 == text2