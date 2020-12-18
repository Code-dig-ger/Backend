# Difficulty section 
# name , prob_id, url , platform = 'C' , difficulty 

# Tag 
# prob_id = id 
# l = list ( problem.tag )
# l.append(new_tag)
# problem.tags = l
# problem.save

# Contest 
# prob_id = id
# problem.contest = contest_id (DEC19A/B)
# problem.save

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from time import sleep

import os,json,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codedigger.settings")
django.setup()
from problem.models import Problem
platform = "C"


def tagsScraper():
    display = Display(visible=0, size=(800, 800))  
    display.start()
    url = "https://www.codechef.com/tags/problems/?itm_medium=navmenu&itm_campaign=tagsproblems"
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(3)
    tagBtn = driver.find_element_by_xpath('//*[@id="tags_filter"]')
    prblmBtn = driver.find_element_by_xpath('//*[@id="problem_count"]')
    tagBtn.click()
    prblmBtn.click()
    prblmBtn.click()
    r = driver.page_source
    soup = BeautifulSoup(r, 'html5lib')
    # print (soup.prettify)

    # Storage 
    majorTags = []

    for tag in soup.findAll('div', class_ = "problem-tagbox"):
        tagPart = tag.text.strip().split()
        # print(tagPart[0])
        # print(int(tagPart[-1]))
        if int(tagPart[-1]) >= 13:
            majorTags.append(tagPart[0])
        else:
            break

    print(len(majorTags))

    for ta in majorTags:
        # url for tags 
        tUrl = f"https://www.codechef.com/tags/problems/{ta}"

        print(tUrl)

        b_url = "https://www.codechef.com"

        # Accessing page

        driver.get(tUrl)
        sleep(5)
        r = driver.page_source

        soup = BeautifulSoup(r, 'html5lib')
        
        for prob in soup.findAll('div', class_='problem-tagbox-inner'):
            name = prob.find('a').text
            link = prob.find('a').get('href')
            name = name.split(" - ")
            prob_id = name[1]
            title = name[0]
            link = b_url+link
            try:
                pro = Problem.objects.get(prob_id = prob_id, platform = "C")
            except Problem.DoesNotExist:
                pro = None
            t = []
            for t1 in prob.findAll('div', class_='actual_tag'):
                t.append(t1.text.strip())

            if pro:
                pro.tags = t
                pro.save()
            else:
                if title != "":
                    Problem.objects.create(name=title,prob_id=prob_id,url = link,tags = t,platform=platform)                
                else:
                    Problem.objects.create(name=prob_id,prob_id=prob_id,url = link,tags = t,platform=platform)                
                    
    driver.quit()        


def longChallenge(b_url, div, mon, yr):
    print("longchallenge started")
    display = Display(visible=0, size=(800, 800))  
    display.start()
    driver = webdriver.Chrome()
    for y in yr:
        for m in mon:
            for d in div:
                # driver.get(url+m+y+d)
                if y == "18" and (m == "JAN" or m == "FEB"):
                    if(d == "B"):
                        continue
                    cont = m+y
                    driver.get(b_url+cont)
                else:
                    cont = m+y+d
                    driver.get(b_url+cont)

                sleep(5)
                r = driver.page_source
                soup = BeautifulSoup(r, 'html5lib')
                storeProb(soup,cont,b_url)
    driver.quit()
                
def lunchTime(b_url, div):
    print("lunch time started")
    display = Display(visible=0, size=(800, 800))  
    display.start()
    driver = webdriver.Chrome()
    latestLunch = 90
    while latestLunch > 57:
        for d in div:
            cont = "LTIME"+str(latestLunch)+d
            driver.get(b_url+cont)
            sleep(3)
            r = driver.page_source
            soup = BeautifulSoup(r, 'html5lib')
            storeProb(soup, cont, b_url)
        latestLunch = latestLunch-1
    driver.quit()

def cookOff(b_url, div):
    print("cookOFF started")
    display = Display(visible=0, size=(800, 800))  
    display.start()
    driver = webdriver.Chrome()
    latestOff = 124
    while latestOff > 91:
        for d in div:
            cont = "COOK"+str(latestOff)+d
            driver.get(b_url+cont)
            sleep(3)
            r = driver.page_source
            soup = BeautifulSoup(r, 'html5lib')
            storeProb(soup, cont, b_url)
        latestOff = latestOff-1
    driver.quit()

def storeProb(soup, cont, b_url):
    problems = soup.findAll('a', class_="ember-view")
    for prob in problems[4:]:
        n = prob.text.strip()
        u = b_url[:-1] + prob.get('href')
        c = prob.get('href').split('/')[-1]
        try:
            p = Problem.objects.get(prob_id=c, platform=platform)
        except Problem.DoesNotExist:
            p = None
        
        if (not p):
            if cont[-1] == "B":
                Problem.objects.create(name=n, prob_id = c, url = u, index = cont, platform=platform)
            else:
                Problem.objects.create(name=n, prob_id = c, url = u, contest_id = cont, platform=platform)
        else:
            if cont[-1] == "B":
                p.index = cont
                p.save()
            else:
                p.contest_id = cont
                p.save()


def contestIdScraper():
    div = ["A", "B"]
    yr = ["18", "19", "20"]
    mon = ["JAN", "FEB", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUG", "SEPT", "OCT", "NOV", "DEC"]
    b_url = "https://www.codechef.com/"
    longChallenge(b_url, div, mon, yr)
    lunchTime(b_url, div)
    cookOff(b_url, div)
    

def codeChefScraper():
    levels = ["school/", "easy/", "medium/", "hard/", "challenge/", "extcontest/"]
    f_url = "https://www.codechef.com/problems/"
    b_url = "https://www.codechef.com"

    # Acessing each level page

    for level in levels:
        # requesting site for data 
        r = requests.get(f_url+level)
        soup = BeautifulSoup(r.content, 'html5lib')
        problemRow = soup.findAll('tr', class_="problemrow")
        print(level)
        for pr in problemRow:
            data = pr.findAll('td')
            if level == 'school/':
                difficulty = "B"
            elif level == 'extcontest/':
                difficulty = ""
            else:
                difficulty = level[0].upper()

            url = b_url + data[0].find('a').get('href')
            name = data[0].text.replace("  ","").replace('\n',"")
            prob_id = data[1].text
            index = ""
            contest_id = ""
            rating = ""
            tags = []
            try:
                p = Problem.objects.get(prob_id = prob_id, platform = platform)
            except Problem.DoesNotExist:
                p = None
            if (not p):
                Problem.objects.create(name=name,prob_id=prob_id,url = url,tags = tags,contest_id=contest_id,rating=rating,platform=platform,index=index,difficulty=difficulty)           
    tagsScraper()   
    contestIdScraper()