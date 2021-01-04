import json
import re
import requests
from bs4 import BeautifulSoup as bs
from codeforces.models import organization , country

def get_atcoder_profile(handle):
    url = "https://atcoder.jp/users/"+handle
    data = {
        'status' : 'FAILED',
        'handle' : handle, 
        'url' : url,
        'rating' : 'UnRated', 
        'rank' : '20 Kyu',
        'color' : '#000000',
        'maxRating' : 'NA',
        'maxRank' : '20 Kyu',
        'maxColor' : '#000000',
        'worldRank' : 'NA',
        'solvedCount' : 'NA',
        'contestRank' : []
    }
    res = requests.get(url)
    if res.status_code != 200 :
        return data
    soup = bs(res.content , 'html5lib')
    ColorCode = { 
        'user-red' : '#FF0000',
        'user-orange': '#FF8000',
        'user-yellow': '#C0C000' ,
        'user-blue' : '#0000FF',
        'user-cyan' : '#00C0C0',
        'user-green' : '#008000',
        'user-brown' : '#804000',
        'user-gray' : '#808080',
        'user-unrated' : '#000000',
        'user-admin' : '#C000C0' 
    }
    grp = soup.find('a' , {'class' : 'username'}).find('span').get('class')
    if grp == None :
        data['color'] = soup.find('a' , {'class' : 'username'}).find('span').get('style')
    else :
        data['color'] = ColorCode[grp[0]]

    if grp!=None and 'unrated' in grp[0] :
        data['rating'] = 'UnRated'
    elif soup.find('div' , {'class' : 'col-md-3 col-sm-12'}).find('b') == None:
        data['rank'] = '20 Kyu'
    else :
        data['rank'] = soup.find('div' , {'class' : 'col-md-3 col-sm-12'}).find('b').text

    del grp
    if data['rating'] != 'unrated': 
        details = soup.findAll('table' , {'class' : 'dl-table'})[1].findAll('tr')
        data['worldRank'] = details[0].find('td').text[:-2]
        data['rating'] = details[1].find('span').text
        data['maxRating'] = details[2].findAll('span')[0].text
        data['maxColor'] = ColorCode[details[2].findAll('span')[0].get('class')[0]]
        data['maxRank'] = details[2].findAll('span')[2].text
        del details
    
    # Contests Rank
    url = "https://atcoder.jp/users/" + handle+ "/history"
    res = requests.get(url)

    if res.status_code != 200 :
        return data
    
    soup = bs(res.content , 'html5lib')
    contestTable = soup.find('table' , {'id' : 'history'})
    del soup
    contests_details = []
    if contestTable != None :
        contests = contestTable.find('tbody').findAll('tr')
        del contestTable
        for contest in contests :
            contest_detail = {}
            base_url = "https://atcoder.jp"
            contest_detail['name'] = contest.findAll('td')[1].find('a').text
            contest_detail['url'] = base_url + contest.findAll('td')[1].find('a')['href']
            contest_detail['code'] = contest.findAll('td')[1].find('a')['href'].split('/')[-1]
            contest_detail['standing_url'] = base_url + contest.findAll('td')[2].find('a')['href']
            rnk = contest.findAll('td')[2].find('a').text
            if rnk.isdigit() :
                contest_detail['worldRank'] = int(rnk)
                contests_details.append(contest_detail)
        del contests
        data['contestRank'] = sorted(contests_details, key = lambda i: i['worldRank'])[:3]
        del contests_details
        
    url = "https://kenkoooo.com/atcoder/atcoder-api/results?user="+handle
    res = requests.get(url)
    if res.status_code != 200:
        return data
    
    d = res.json()
    cnt = 0
    for x in d : 
        cnt += (x['result'] == 'AC') 
    data['solvedCount'] = cnt
    data['status']  = 'OK'
    return data

def get_spoj_profile(handle):
    url = "https://www.spoj.com/users/" + handle
    res = requests.get(url)
    data = {
        'status' : 'FAILED',
        'handle' : handle ,
        'url' : url , 
        'worldRank' : 'NA',
        'solvedCount' : 'NA' , 
        'points' : 'NA',
    }
    if res.status_code != 200:
        return data
    soup = bs(res.content , 'html5lib')

    data['solvedCount'] = soup.find('dl' , {'class' : 'dl-horizontal profile-info-data profile-info-data-stats'}).find('dd').text

    rank = None 
    y = soup.find('div' , {'id' : 'user-profile-left'}).findAll('p')
    del soup
    for x in y:
        if x.find('i' ,{'class' : 'fa fa-trophy'}) != None :
            rank = x.text
            break
    
    if x == None :
        return data
    
    data['worldRank'] = rank.replace(' World Rank: #' , '').split(' ')[0]
    data['points'] = rank.replace(' World Rank: #' , '').split(' ')[1][1:]
    data['status']  = 'OK'
    return data

def get_uva_profile(uva_id , handle):
    url = "https://uhunt.onlinejudge.org/api/ranklist/"+ str(uva_id) +"/0/0"
    res = requests.get(url)
    data = {
        'status' : 'FAILED',
        'handle' : handle ,
        'uva_id' : uva_id , 
        'url' : 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=19&page=show_authorstats&userid=' + str(uva_id),
        'worldRank' : 'NA',
        'solvedCount' : 'NA',
    }
    if res.status_code != 200 :
        return
    d = res.json()[0]
    data['worldRank'] = d['rank']
    data['solvedCount'] = d['ac']
    data['status']  = 'OK'
    return data

def get_color(rating):
    if rating < 1400 :
        return '#666666'
    elif rating < 1600 :
        return '#1E7D22'
    elif rating < 1800 :
        return '#3366CC'
    elif rating < 2000 :
        return '#684273'
    elif rating < 2200 :
        return '#FFBF00'
    elif rating < 2500 :
        return '#FF7F00'
    else :
        return '#D0011B'

def get_rank(rating):
    if rating < 1400 :
        return 1
    elif rating < 1600 :
        return 2
    elif rating < 1800 :
        return 3
    elif rating < 2000 :
        return 4
    elif rating < 2200 :
        return 5
    elif rating < 2500 :
        return 6
    else :
        return 7
    
def get_codechef_profile(handle):
    
    url = "https://www.codechef.com/users/" + handle
    data = {
        'status' : 'FAILED',
        'handle' : handle, 
        'name' : '',
        'url': url,
        'rating' : 'UnRated', 
        'maxRating': 'NA',
        'rank' : 'NA',
        'maxRank' : 'NA',
        'color' : '#000000',
        'maxColor' : '#000000',
        'worldRank' : 'NA',
        'countryRank' : 'NA',
        'solvedCount' : 'NA',
        'contestRank' : [],
    }
    
    res = requests.get(url)
    if res.status_code != 200 :
        return data

    soup = bs(res.content ,'html5lib')
    
    header = soup.find('div' , {'class' : 'user-details-container'})
    
    if header != None :
        if header.find('h2') != None :
            data['name'] = header.find('h2').text
    
    data['rating'] = int(soup.find('div' , {'class' : 'rating-number'}).text)
    data['rank'] = get_rank(data['rating'])
    data['color'] = get_color(data['rating'])
    
    data['maxRating'] = int(soup.find('div' , {'class' : 'rating-header'}).find('small').text.replace('(Highest Rating ' , '').replace(')',''))
    data['maxRank'] = get_rank(data['maxRating'])
    data['maxColor'] = get_color(data['maxRating'])
    
    # Ranks
    rank = soup.find('div' , {'class' : 'rating-ranks'})
    data['worldRank'] = rank.findAll('strong')[0].text
    data['countryRank'] = rank.findAll('strong')[1].text
    
    finding_rating = re.findall(r'var all_rating = .*;', str(soup))
    finds = len(finding_rating) == 1

    if finds :
        s = finding_rating[0].replace('var all_rating = ' , '').replace(';' , '')
        contest_details = json.loads(s)
        del s 
        del finding_rating
    
    lunch = []
    cook = []
    challenge = []
    overall = []

    for contest in contest_details :
        if contest['rank'].isdigit() :
            overall.append({
                'name' : contest['name'],
                'code' : contest['code'],
                'standingUrl' : 'https://www.codechef.com/rankings/{}?order=asc&search={}&sortBy=rank'.format(contest['code'] , handle),
                'url' :  'https://www.codechef.com/' + contest['code'], 
                'rank' : int(contest['rank'])
            })
            if 'Challenge' in contest['name'] :
                challenge.append({
                    'name' : contest['name'],
                    'code' : contest['code'],
                    'standingUrl' : 'https://www.codechef.com/rankings/{}?order=asc&search={}&sortBy=rank'.format(contest['code'] , handle),
                    'url' :  'https://www.codechef.com/' + contest['code'], 
                    'rank' : int(contest['rank'])
                })
            elif 'Cook' in contest['name'] :
                cook.append({
                    'name' : contest['name'],
                    'code' : contest['code'],
                    'standingUrl' : 'https://www.codechef.com/rankings/{}?order=asc&search={}&sortBy=rank'.format(contest['code'] , handle),
                    'url' :  'https://www.codechef.com/' + contest['code'], 
                    'rank' : int(contest['rank'])
                })
            elif 'Lunchtime' in contest['name'] :
                lunch.append({
                    'name' : contest['name'],
                    'code' : contest['code'],
                    'standingUrl' : 'https://www.codechef.com/rankings/{}?order=asc&search={}&sortBy=rank'.format(contest['code'] , handle),
                    'url' :  'https://www.codechef.com/' + contest['code'], 
                    'rank' : int(contest['rank'])
                })


    data['contestRank'] = sorted(overall, key = lambda i: i['rank'])[:3]
    data['lunchtimeRank'] = sorted(lunch , key = lambda i: i['rank'])[:3]
    data['cook-offRank'] = sorted(cook , key = lambda i: i['rank'])[:3]
    data['longChallengeRank'] = sorted(challenge , key = lambda i: i['rank'])[:3]

    problems_solved = soup.find('section' , {'class' : 'rating-data-section problems-solved'})

    del soup
    
    data['solvedCount'] = problems_solved.find('h5').text.replace('Fully Solved (' , '').replace(')' ,'')
    data['status']  = 'OK'
    return data

def get_codeforces_profile(handle , codeforces_user=None) :

    url = "https://codeforces.com/api/user.info?handles=" + handle

    profileurl = "https://codeforces.com/profile/" + handle

    res = requests.get(url)

    extra_data = {
        'handle' : handle ,
        'url' : profileurl , 
        'name' : '',
        'rating' : 'UnRated',
        'rank' : 'NA',
        'maxRating' : 'NA',
        'maxRank' : 'NA',
        'country' : None,
        'organization' : None,
        'photoUrl' : None,
        'totalUsers' : 'NA',
        'worldRank' : 'NA',
        'countryRank' : 'NA',
        'organizationRank' : 'NA',
        'contestRank' : [],
        'status' : 'FAILED',
        'contribution' : 'NA',
        'avatar' : None,
        'lastOnlineTimeSeconds' : 0,
        'friendOfCount' : 'NA', 
    }

    if res.status_code != 200 :
        return (codeforces_user, extra_data) 

    d = res.json()

    if d['status'] != 'OK' :
        return (codeforces_user, extra_data) 

    extra_data['status'] = 'OK'
    extra_data['contribution'] = d['result'][0]['contribution']
    extra_data['photoUrl'] = d['result'][0]['titlePhoto'][2:]
    extra_data['avatar'] = d['result'][0]['avatar'][2:]
    extra_data['lastOnlineTimeSeconds'] = d['result'][0]['lastOnlineTimeSeconds']
    extra_data['friendOfCount'] = d['result'][0]['friendOfCount']

    name = ""
    if 'firstName' in d['result'][0]:
        name += d['result'][0]['firstName']
        name += " "
    if 'lastName' in d['result'][0]:
        name += d['result'][0]['lastName']

    extra_data["name"] = name

    if 'rating' not in d['result'][0] : 
        extra_data['rating'] = 'UnRated'
        return (codeforces_user, extra_data) 
    elif codeforces_user == None :
        
        extra_data['rating'] = d['result'][0]['rating']
        extra_data['maxRating'] = d['result'][0]['maxRating']
        extra_data['rank'] = d['result'][0]['rank']
        extra_data['maxRank']  = d['result'][0]['maxRank']

        if 'country' in d['result'][0] :

            extra_data['country'] = { 'name' : d['result'][0]['country'] }

        if 'organization' in d['result'][0] :

            extra_data['organization']  =  { 'name' : d['result'][0]['organization'] }

        return (codeforces_user, extra_data) 
    else :

        codeforces_user.name = name     
        codeforces_user.rating = d['result'][0]['rating']
        codeforces_user.maxRating = d['result'][0]['maxRating']
        codeforces_user.rank = d['result'][0]['rank']
        codeforces_user.maxRank  = d['result'][0]['maxRank']
        codeforces_user.photoUrl = d['result'][0]['titlePhoto'][2:]

        if 'country' in d['result'][0] :

            obj, created = country.objects.get_or_create(name=  d['result'][0]['country'] )
            codeforces_user.country = obj

        if 'organization' in d['result'][0] :

            obj, created = organization.objects.get_or_create(name=  d['result'][0]['organization'] )
            codeforces_user.organization = obj

        codeforces_user.save()

        return (codeforces_user, extra_data) 







