import pickle
import threading
import time
import sqlite3
from sqlite3 import Error
import requests
import threading
import time
import random
import html
import pickle
from bs4 import BeautifulSoup
from textblob import TextBlob
from gensim.summarization.summarizer import summarize
from collections import OrderedDict
import sys
import os
from googletrans import Translator

WORLD_NEWS_PICKLE_FILE = 'pickles/world.p'
POLITICS_NEWS_PICKLE_FILE = 'pickles/politics.p'
SPORTS_NEWS_PICKLE_FILE = 'pickles/sports.p'
BOLLYWOOD_NEWS_PICKLE_FILE = 'pickles/bollywood.p'
FAKE_NEWS_PICKLE_FILE = 'pickles/fakenews.p'
NATIONAL_NEWS_PICKLE_FILE = 'pickles/national.p'
TECH_NEWS_PICKLE_FILE = 'pickles/tech.p'
KARNATAKA_NEWS_PICKLE_FILE = 'pickles/karnataka.p'
WESTBENGAL_NEWS_PICKLE_FILE = 'pickles/westbengal.p'
MAHARASHTRA_NEWS_PICKLE_FILE = 'pickles/maharashtra.p'
GUJARAT_NEWS_PICKLE_FILE = 'pickles/gujarat.p'
ANDHRAPRADESH_NEWS_PICKLE_FILE = 'pickles/andhrapradesh.p'
RAJASTHAN_NEWS_PICKLE_FILE = 'pickles/rajasthan.p'
TRENDING_NEWS_PICKLE_FILE = 'pickles/trending.p'
UTTARPRADESH_NEWS_PICKLE_FILE = 'pickles/uttarpradesh.p'
DELHI_NEWS_PICKLE_FILE = 'pickles/delhi.p'
UTTARPRADESH_DISTRICT_NEWS_PICKLE_FILE = 'pickles/uttarpradesh_district.p'
MAHARASHTRA_DISTRICT_NEWS_PICKLE_FILE = 'pickles/maharashtra_district.p'
KARNATAKA_DISTRICT_NEWS_PICKLE_FILE = 'pickles/karnataka_district.p'
WESTBENGAL_DISTRICT_NEWS_PICKLE_FILE = 'pickles/westbengal_district.p'
GUJARAT_DISTRICT_NEWS_PICKLE_FILE = 'pickles/gujarat_district.p'
ANDHRAPRADESH_DISTRICT_NEWS_PICKLE_FILE = 'pickles/andhrapradesh_district.p'
RAJASTHAN_DISTRICT_NEWS_PICKLE_FILE = 'pickles/rajasthan_district.p'
ALLOWED_LANGUAGES = ['hi', 'kn', 'mr','bn','gu','te','ta','ml','pa','ur']
POST_URL = 'http://newfinder.pythonanywhere.com/postinfo'
N = 23
UTTARPRADESH_DISTRICTS=['lucknow','varanasi','bareilly','moradabad','meerut','agra','aligarh','prayagraj','gorakhpur','kanpur','barabanki','azamgarh']
KARNATAKA_DISTRICTS=['bangalore','mysore','udupi','shimoga','belgaum','mangalore',"other-cities", 'belagavi']
MAHARASHTRA_DISTRICTS =['mumbai','pune','nagpur','aurangabad','nashik','solapur','kolhapur','thane','ratnagiri', 'jalgaon', 'ahmednagar']
WESTBENGAL_DISTRICTS=['alipurduar','cooch-behar','darjeeling','jalpaiguri','kalimpong','siliguri','kolkata','purulia','khadagpur']
GUJARAT_DISTRICTS=['ahmedabad','baroda','bhavnagar','kutch-bhuj','rajkot','surat','patan-banaskantha','mehsana','vadodara']
ANDHRAPRADESH_DISTRICTS=['visakhapatnam','amaravati','ananthapur','chittoor','eastgodavari','guntur','krishna','kurnool','psr-nellore','srikakulam','vizianagaram','westgodavari','ysr']
RAJASTHAN_DISTRICTS=['jaipur','jodhpur','kota','udaipur','bikaner','ajmer','bharatpur','sri-ganganagar','jaisalmer','jhunjhunu','churu','alwar','dungarpur','bhilwara','chittorgarh']
global_lock = threading.Lock()


#########################################################
#                                                       #
#               START WORLD NEWS SCRAPER                #
#                                                       #
#########################################################


ScrapedData = dict()
def write_to_file(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData.update(subdict)
    global_lock.release()
def Shorten(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def IndiaTodayGatherData(i, PostHeading, Url, subdict):
    try:
        PostUrl = "https://www.indiatoday.in"+Url
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostImageAddress = Postsoup.find(
            'div', class_="stryimg").find('img')['data-src']
        PostArticle = Postsoup.find('div', class_='description')
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text.replace('.', '. ')
        Summary = Shorten(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("----->isme error aya", PostHeading)
def ReutersGatherData(i, PostHeading, Url, subdict):
    try:
        PostUrl = "https://www.reuters.com"+Url
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='StandardArticleBody_body')
        PostImageAddress = PostArticle.find('img')
        if PostImageAddress is not None:
            PostImageAddress = PostImageAddress['src']
            PostImageAddress = "https://" + PostImageAddress[2:-2]+"1600"
        else:
            return

        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text.replace('.', '. ')
        Summary = Shorten(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("----->isme error aya", PostHeading)
def ndtvGatherData(i, PostHeading, Url, subdict):
    try:
        PostUrl = Url
        PortReq = requests.get(Url).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', id='ins_storybody')
        PostImageAddress = PostArticle.find('img')['data-src']
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text.replace('.', '. ')
        Summary = Shorten(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("----->isme error aya", PostHeading)
def EconomicsTimesGatherData(i, PostHeading, Url, subdict):
    try:
        PostUrl = "https://economictimes.indiatimes.com"+Url
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='article_block')
        PostImageAddress = PostArticle.find(
            'div', class_="articleImg midImg").find('img')['src']
        PostComplete = PostArticle.find('div', class_='Normal')
        for script in PostComplete(["script", "style"]):
            script.decompose()
        PostComplete = PostComplete.get_text().replace("\n", "").replace('.', '. ')
        Summary = Shorten(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("----->isme error aya", PostHeading)
def ZeeNewsGatherData(i, PostHeading, Url, subdict):
    try:
        PostUrl = "https://zeenews.india.com"+Url
        agent = {"User-Agent": "Mozilla/5.0"}
        PortReq = requests.get(PostUrl, headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='content')
        PostImageAddress = PostArticle.find(
            'img', class_="img-responsive")['src']
        PostArticle = PostArticle.find('div', class_='article')
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text
        PostComplete = PostComplete.replace("\n", "").replace('.', '. ')
        Summary = Shorten(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("----->isme error aya", PostHeading)
def ScrapIndiaToday(d, isNewsPickle):
    c = 0
    subdict = OrderedDict()
    flag = -1
    #address = "https://www.indiatoday.in/world"
    count = 0
    while(c < 3):
        if c == 0:
            URL = "https://www.indiatoday.in/world"
        else:
            URL = "https://www.indiatoday.in/world?page="+str(c)
        c += 1
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='view-content')
        for i in article.findAll('div', class_='catagory-listing'):
            count += 1
            PostHeading = i.find('h2')['title']
            PostUrl = i.find('a')['href']
            if isNewsPickle == 1:
                if PostHeading not in d:
                    IndiaTodayGatherData(i, PostHeading, PostUrl, subdict)
                else:
                    flag = 1
                    print(
                        "----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                IndiaTodayGatherData(i, PostHeading, PostUrl, subdict)
        if flag == 1:
            break
    print(len(subdict), "artiles updated in from indiatoday")

    # reversing the dict for restoring the order
    # subdict = OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file(subdict)
def ScrapReuters(d, isNewsPickle):
    c = 1
    subdict = OrderedDict()
    flag = -1
    #address = "https://www.reuters.com/news/archive/worldNews"
    count = 0
    while(c < 3):
        if c == 1:
            URL = "https://www.reuters.com/news/archive/worldNews"
        else:
            URL = "https://www.reuters.com/news/archive/worldNews?view=page&page=" + \
                str(c)+"&pageSize=10"
        c += 1
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='news-headline-list')
        for i in article.findAll('article', class_='story'):
            count += 1
            PostHeading = i.find('h3').text.strip()
            PostUrl = i.find('a')['href']
            if isNewsPickle == 1:
                if PostHeading not in d:
                    ReutersGatherData(i, PostHeading, PostUrl, subdict)
                else:
                    flag = 1
                    print(
                        "----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                ReutersGatherData(i, PostHeading, PostUrl, subdict)
        if flag == 1:
            break
    # subdict = OrderedDict(reversed(list(subdict.items())))
    print(len(subdict), "artiles updated in from reuters")
    write_to_file(subdict)
def Scrapndtv(d, isNewsPickle):
    c = 1
    subdict = OrderedDict()
    flag = -1
    count = 0
    while(c < 3):
        URL = "https://www.ndtv.com/world-news/page-"+str(c)
        c += 1
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='new_storylising')
        for i in article.findAll('div', class_='new_storylising_contentwrap'):
            count += 1
            PostHeading = i.find('a')['title']
            PostUrl = i.find('a')['href']
            if isNewsPickle == 1:
                if PostHeading not in d:
                    ndtvGatherData(i, PostHeading, PostUrl, subdict)
                else:
                    flag = 1
                    print(
                        "----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                ndtvGatherData(i, PostHeading, PostUrl, subdict)
        if flag == 1:
            break
    # subdict = OrderedDict(reversed(list(subdict.items())))
    print(len(subdict), "artiles updated in from ndtv")
    write_to_file(subdict)
def ScrapEconomicsTimes(d, isNewsPickle):
    #c = 1
    subdict = OrderedDict()
    # flag = -1
    count = 0
    URL = "https://economictimes.indiatimes.com/news/international/world-news"
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('div', class_='tabdata')
    for i in article.findAll('div', class_='eachStory'):
        count += 1
        PostUrl = i.find('a')['href']
        PostHeading = i.find('h3').text
        if isNewsPickle == 1:
            if PostHeading not in d:
                EconomicsTimesGatherData(i, PostHeading, PostUrl, subdict)
            else:
                flag = 1
                print("----->bas itna hi update hua hai.... baki apne paas already hai")
                break
        else:
            EconomicsTimesGatherData(i, PostHeading, PostUrl, subdict)

    # subdict = OrderedDict(reversed(list(subdict.items())))

    print(len(subdict), "artiles updated in from Economics times se")
    write_to_file(subdict)
def ScrapZeeNews(d, isNewsPickle):
    c = 1
    subdict = OrderedDict()
    flag = -1
    address = "https://zeenews.india.com/world"
    count = 0
    while(c < 2):
        if c == 1:
            URL = address
        else:
            URL = address+"?page="+str(c-1)
        c += 1
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('section', class_='maincontent')
        for i in article.findAll('div', class_="section-article margin-bt30px clearfix"):
            count += 1
            PostHeading = i.find('a').find('img')['title']
            PostUrl = i.find('a')['href']
            if isNewsPickle == 1:
                if PostHeading not in d:
                    ZeeNewsGatherData(i, PostHeading, PostUrl, subdict)
                else:
                    flag = 1
                    print(
                        "----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                ZeeNewsGatherData(i, PostHeading, PostUrl, subdict)
        if flag == 1:
            break

    #subdict = OrderedDict(reversed(list(subdict.items())))

    print(len(subdict), "artiles updated in from ZeeNews")

    write_to_file(subdict)
def ScrapSuper(i, d, isNewsPickle):
    if i == 0:
        ScrapZeeNews(d, isNewsPickle)
    elif i == 1:
        ScrapEconomicsTimes(d, isNewsPickle)
    elif i == 2:
        Scrapndtv(d, isNewsPickle)
    elif i == 3:
        ScrapReuters(d, isNewsPickle)
    else:
        ScrapIndiaToday(d, isNewsPickle)
def scrape_world_news(langauges, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(5):
            p = threading.Thread(target=ScrapSuper, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData))
        post_data = {"news_type": "world_news", "news": []}
        for data in ScrapedData.values():
            post_data["news"].append({"english": [html.unescape(html.unescape(data[2].replace("\n", " "))), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in langauges]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#                END WORLD NEWS SCRAPER                 #
#                                                       #
#########################################################


#########################################################
#                                                       #
#            START NATIONAL NEWS SCRAPER                #
#                                                       #
#########################################################



ScrapedData2 = dict()
def write_to_file2(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData2.update(subdict)
    global_lock.release()
def Shorten2(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataJagran2(i, d, PostHeading, subdict, translator):
    try:
        # andre wali post ka url
        PostUrl = "https://english.jagran.com/"+i.find('a')['href']
        print(PostUrl)
        # post image ka url
        PostImageAddress = i.find('img')['data-src']
        if not PostImageAddress.startswith('http'):
            PostImageAddress = "https:" + i.find('img')['data-src']
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='articleBody')
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text
        # translator = Translator()
        PostComplete = translator.translate(
            PostComplete, src='hi', dest='en').text
        Summary = Shorten2(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        pass
def ScrapeJagran2(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://english.jagran.com/india-page" + str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('ul', class_='topicList')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            value = (float(time.time())-clock)
            print(count, value)
            count += 1
            try:
                PostHeading = i.find("img", class_='lazy')["alt"]
                PostHeading = translator.translate(
                    PostHeading, src='hi', dest='en').text
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataJagran2(i, d, PostHeading, subdict, translator)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran2(i, d, PostHeading, subdict, translator)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Jagaran")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file2(subdict)
def GatherDataLiveHindustan2(i, d, subdict, PostHeading, translator):
    try:
        PostUrl = "https://www.livehindustan.com"+i.find('a')['href']
        print(PostUrl)
        # PostHeading=i.find('img')['title']
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(PostUrl, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='story-page-content')
        PostComplete = ""
        for j in article.findAll('p'):
            PostComplete += j.text
        PostImageAddress = soup.find(
            'div', class_='carousel-inner story-page-inner carousel-Sec story-detail-img').find('img')['data-src']
        PostComplete = translator.translate(PostComplete, src='hi', dest='en').text
        Summary = Shorten2(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeLiveHindustan2(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 5):
        URL = "https://www.livehindustan.com/national/news-"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find(
            'ul', class_='right-top-news no-pad personality-celebrity listing-widgets-content')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                PostHeading = translator.translate(
                    PostHeading, src='hi', dest='en').text
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataLiveHindustan2(i, d, subdict, PostHeading, translator)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveHindustan2(i, d, subdict, PostHeading, translator)
            except:
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Live Hindustan")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file2(subdict)
def GatherDataZeeNews2(i, d, subdict):
    try:
        PostUrl = "https://zeenews.india.com"+i.find('a')['href']
        PostHeading = i.find('img')['title']
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(PostUrl, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='article-right-col main')
        PostComplete = ""
        for j in article.findAll('p'):
            PostComplete += j.text
        PostImageAddress = soup.find(
            'div', class_='article-image-block margin-bt30px').find('img')['src']
        Summary = Shorten2(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("iss mai error aaya")
def ScrapeZeeNews2(d, isNewsPickle):
    c = 0
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://zeenews.india.com/india"
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('section', class_='maincontent')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('div', class_="section-article margin-bt30px clearfix"):
            try:
                if c >= 60:
                    break
                c += 1
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataZeeNews2(i, d, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews2(i, d, subdict)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Zee News")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file2(subdict)
def ScrapSuper2(i, d, isNewsPickle):
    if i == 0:
        ScrapeJagran2(d, isNewsPickle)
    elif i == 1:
        ScrapeLiveHindustan2(d, isNewsPickle)
    elif i == 2:
        ScrapeZeeNews2(d, isNewsPickle)
def scrape_national_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper2, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData2))
        post_data = {"news_type": "national_news", "news": []}
        for data in ScrapedData2.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData2.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#              END NATIONAL NEWS SCRAPER                #
#                                                       #
#########################################################


#########################################################
#                                                       #
#            START KARNATAKA NEWS SCRAPER               #
#                                                       #
#########################################################



ScrapedData3 = dict()
def write_to_file3(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData3.update(subdict)
    global_lock.release()
def Shorten3(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def NewsKarnatakaGatherData3(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='news_detail')
        PostImageAddress="https://www.newskarnataka.com/"+PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten3(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapNewsKarnataka3(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    URL="https://www.newskarnataka.com/karnataka"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='listed_news two_col_list classified_list inner')
        for i in article.findAll('li'):
            try:
                count+=1
                PostHeading=i.find('a')['title']
                PostUrl=i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        NewsKarnatakaGatherData3(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    NewsKarnatakaGatherData3(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ")
    write_to_file3(subdict)
def PrajavaniGatherData3(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='content')
        PostImageAddress=PostArticle.find('div',class_='field field-name-field-image field-type-image field-label-hidden').find('div',class_='field-items').find('div',class_='field-item even').find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        translator=Translator()
        Summary=Shorten3(PostComplete,PostHeading)
        Summary=translator.translate(Summary,src='kn',dest='en').text
        t=Translator()
        Summary=t.translate(Summary,dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapPrajavani3(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.prajavani.net/karnataka-news"
    #newspicle_pehle_se_hai?
    count=0
    c=0
    while(c<1):
        c+=1
        URL =address
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='group')
        for i in article.findAll('div',class_='pj-top-trending__img-wrapper'):
            count+=1
            PostUrl="https://www.prajavani.net"+i.find('a')['href']
            PostHeading=i.find('a').find('img')['alt']
            translator=Translator()
            PostHeading=translator.translate(PostHeading,src='kn',dest='en').text
            if isNewsPickle==1:
                if PostHeading not in d:
                    PrajavaniGatherData3(i,PostHeading,PostUrl,subdict)
                else:
                    flag=1
                    print("----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                PrajavaniGatherData3(i,PostHeading,PostUrl,subdict)
        if flag==1:
            break
    print(len(subdict),"artiles updated in from prajavani in ")
    write_to_file3(subdict)
def GatherDataJagran3(i, d, subdict, PostHeading, translator):
    try:
        # andre wali post ka url
        PostUrl = "https://www.jagran.com"+i.find('a')['href']
        # post image ka url
        PostImageAddress = i.find('img')['data-src']
        if not PostImageAddress.startswith('http'):
                PostImageAddress = "https:" + i.find('img')['data-src']
        # post ki heading
        # PostHeading = i.find('h3').text

        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='articleBody')
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text
        PostComplete = translator.translate(PostComplete, src='hi', dest='en').text
        Summary = Shorten3(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeJagran3(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://www.jagran.com/topics/karnataka-p"+str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('ul', class_='topicList')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):

            value = (float(time.time())-clock)
            print(count, value)
            count += 1
            PostHeading = i.find('h3').text
            PostHeading = translator.translate(
                PostHeading, src='hi', dest='en').text
            try:
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataJagran3(i, d, subdict, PostHeading, translator)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran3(i, d, subdict, PostHeading, translator)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Jargan")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file3(subdict)
def GatherDataLiveHindustan3(i, d, subdict, PostHeading, translator):
    try:
        PostUrl = "https://www.livehindustan.com"+i.find('a')['href']
        print(PostUrl)
        # PostHeading = i.find('img')['title']
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(PostUrl, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='story-page-content')
        PostComplete = ""
        for j in article.findAll('p'):
            PostComplete += j.text
        PostImageAddress = soup.find(
            'div', class_='carousel-inner story-page-inner carousel-Sec story-detail-img').find('img')['data-src']
        PostComplete = translator.translate(PostComplete, src='hi', dest='en').text
        Summary = Shorten3(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("iss mai error aaya -->",PostHeading)
def ScrapeLiveHindustan3(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 5):
        URL = "https://www.livehindustan.com/tags/karnataka/"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find(
            'ul', class_='right-top-news no-pad personality-celebrity listing-widgets-content')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                PostHeading = translator.translate(
                    PostHeading, src='hi', dest='en').text
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataLiveHindustan3(i, d, subdict, PostHeading, translator)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveHindustan3(i, d, subdict, PostHeading, translator)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Live Hindustan")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file3(subdict)
def GatherDataZeeNews3(i, d, subdict):
    try:
        PostUrl = "https://zeenews.india.com"+i.find('a')['href']
        PostHeading = i.find('img')['title']
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(PostUrl, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='article-right-col main')
        PostComplete = ""
        for j in article.findAll('p'):
            PostComplete += j.text
        PostImageAddress = soup.find(
            'div', class_='article-image-block margin-bt30px').find('img')['src']
        Summary = Shorten3(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("ismai error aaya")
def ScrapeZeeNews3(d, isNewsPickle):
    c = 0
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://zeenews.india.com/tags/karnataka.html-"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('section', class_='maincontent')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('div', class_="section-article margin-bt30px clearfix"):
            try:
                if c >= 60:
                    break
                c += 1
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataZeeNews3(i, d, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews3(i, d, subdict)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Zee News")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file3(subdict)
def ScrapSuper3(i, d, isNewsPickle):
    if i == 0:
        ScrapNewsKarnataka3(d, isNewsPickle)
    elif i == 1:
        ScrapPrajavani3(d, isNewsPickle)
def scrape_state_karnataka_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(2):
            p = threading.Thread(target=ScrapSuper3, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData3))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData3.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'karnataka', None], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData3.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#              END KARNATAKA NEWS SCRAPER               #
#                                                       #
#########################################################



#########################################################
#                                                       #
#           START WESTBENGAL NEWS SCRAPER               #
#                                                       #
#########################################################



ScrapedData15 = dict()
def write_to_file15(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData15.update(subdict)
    global_lock.release()
def Shorten15(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataHindustanTimes15(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='storyDetail')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten15(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("iss mai error aaya -->",PostHeading) 
def ScrapeHindustanTimes15(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<5):
        URL = "https://www.hindustantimes.com/topic/-west-bengal/page-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='mainContent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="authorListing"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes15(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes15(i,d,subdict)
            except Exception as e:
                print("###################################################################################")
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file15(subdict)
def GatherDataDeccanHerald15(i,d,subdict):
    try:
        PostUrl ="https://www.deccanherald.com"+i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="content")
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten15(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("Iss mai error aaya -->",PostHeading)
def ScrapeDeccanHerald15(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<2):
        URL = "https://www.deccanherald.com/tag/west-bengal"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',id='main-content')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['alt']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataDeccanHerald15(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataDeccanHerald15(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file15(subdict)
def GatherDataTelegraphIndia15(i,d,subdict,post):
    try:
        PostUrl ="https://www.telegraphindia.com"+i.find('a')['href']
        print(PostUrl)
        PostHeading=post
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.findAll('div',class_="col-12")[1]
        PostComplete=""
        for j in article.find('div',class_="fs-17 pt-2 noto-regular").findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten15(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except Exception as e:
        print(e)
def ScrapeTelegraphIndia15(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://www.telegraphindia.com/west-bengal/page-"+str(c)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='row uk-grid-divider pb-3')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_='row pb-3 pt-3'):
            try:
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h2').text
                PostHeading=PostHeading.replace(" ","")
                PostHeading=PostHeading.replace("\n","")
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataTelegraphIndia15(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataTelegraphIndia15(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file15(subdict)
def ScrapSuper15(i,d,isNewsPickle):
    if i==0:
        ScrapeDeccanHerald15(d,isNewsPickle)
    elif i==2:
        ScrapeHindustanTimes15(d,isNewsPickle)
    elif i==3:
        ScrapeTelegraphIndia15(d,isNewsPickle)
def scrape_state_westbengal_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(4):
            p = threading.Thread(target=ScrapSuper15, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData15))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData15.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'westbengal', None], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData15.clear()
        time.sleep(1800)    



#########################################################
#                                                       #
#             END WESTBENGAL NEWS SCRAPER               #
#                                                       #
#########################################################



#########################################################
#                                                       #
#             START GUJARAT NEWS SCRAPER                #
#                                                       #
#########################################################



ScrapedData17 = dict()
def write_to_file17(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData17.update(subdict)
    global_lock.release()
def Shorten17(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataHindustanTimes17(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='storyDetail')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten17(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("iss mai error aaya -->",PostHeading)
def ScrapeHindustanTimes17(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<5):
        URL = "https://www.hindustantimes.com/topic/-gujarat/page-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='mainContent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="authorListing"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes17(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes17(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file17(subdict)
def GatherDataJagran17(i,d,subdict,PostHeading):
    try:
    # andre wali post ka url
        PostUrl = "https://www.jagran.com"+i.find('a')['href']
        # post image ka url
        PostImageAddress="https:"+i.find('img')['data-src']

        # post ki heading

        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='articleBody')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten17(PostComplete,PostHeading)
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
        print(PostImageAddress)
    except:
        print("iss mai error aaya -->",PostHeading)  
def ScrapeJagran17(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://www.jagran.com/topics/gujarat-p"+str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h3').text
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src='hi',dest='en').text
                print(PostHeading)
            
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataJagran17(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran17(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")
    write_to_file17(subdict)
def ScrapSuper17(i,d,isNewsPickle):
    if i==0:
        ScrapeJagran17(d,isNewsPickle)
    if i==1:
        ScrapeHindustanTimes17(d,isNewsPickle)
def scrape_state_gujarat_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(2):
            p = threading.Thread(target=ScrapSuper17, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData17))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData17.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'gujarat', None], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData17.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#             END GUJARAT NEWS SCRAPER                  #
#                                                       #
#########################################################


#########################################################
#                                                       #
#     START ANDHRAPRADESH NEWS SCRAPER                  #
#                                                       #
#########################################################


ScrapedData19 = dict()
def write_to_file19(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData19.update(subdict)
    global_lock.release()
def Shorten19(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataGreatAndhra19(i,d,subdict,PostHeading):
    try:
    # andre wali post ka url
        PostUrl = i.find('a')['href']
        print(PostUrl)
        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='content')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        translator = Translator()
    #     PostComplete = translator.translate(PostComplete,src='te',dest='en').text
        Summary=Shorten19(PostComplete,PostHeading)
    #     Summary=translator.translate(Summary,dest='en').text
        PostImageAddress=PostArticle.find('img')['src']
        print(PostImageAddress)
        print(Summary)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
        print(PostImageAddress)
    except:
        print("iss mai error aaya -->",PostHeading)
def ScrapeGreatAndhra19(d,isNewsPickle):
    try:
        c=1
        # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
        subdict=OrderedDict()
        #reprocessing se bachane k liye
        flag=0
        count=0   
        while(c<4):
            URL = "https://www.greatandhra.com/latest/"+str(c)
            r = requests.get(URL).text
            soup = BeautifulSoup(r, 'lxml')
            article=soup.find('div',class_='content')
            count=0
            clock=float(time.time())
            print("start",(float(time.time())-clock))
            for i in article.findAll('div',class_="movies_news_description_container float-left"):
                try:
                    value=(float(time.time())-clock)
                    print(count,value)
                    count+=1
    #                 print(i)
                    PostHeading=i.find('div',class_='img_plc').find('img')['alt']
                    print(PostHeading)
                
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            GatherDataGreatAndhra19(i,d,subdict,PostHeading)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        GatherDataGreatAndhra19(i,d,subdict,PostHeading)
                except Exception as e:
                    print(e)
                    continue
            if flag==1:
                break
            c+=1
        print(len(subdict),"artiles updated in from indiatoday")  
            #reversing the dict for restoring the order
        #subdict=OrderedDict(reversed(list(subdict.items())))
            #picle me dictionary store kr rahe  hai
        write_to_file19(subdict)
    except:
        pass
def GatherDataSamayam19(i,d,subdict,PostHeading):
    try:
    # andre wali post ka url
        PostUrl = i.find('a')['href']
        
        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='story-article')
        PostComplete=PostArticle.text
    #     for j in PostArticle.findAll('p'):
    #         PostComplete+=j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='te',dest='en').text
        Summary=Shorten19(PostComplete,PostHeading)
        Summary=translator.translate(Summary,dest='en').text
        PostImageAddress=PostArticle.find('img')['src']
        print(PostImageAddress)
        print(Summary)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
        print(PostImageAddress)
    except:
        print("iss mai error aaya -->",PostHeading)
def ScrapeSamayam19(d,isNewsPickle):
    try:
        c=1
        # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
        subdict=OrderedDict()
        #reprocessing se bachane k liye
        flag=0
        count=0   
        while(c<4):
            URL = "https://telugu.samayam.com/andhra-pradesh/news/articlelist/70465957.cms?curpg="+str(c)
            r = requests.get(URL).text
            soup = BeautifulSoup(r, 'lxml')
            article=soup.find('ul',class_='col12 pd0 medium_listing')
            count=0
            clock=float(time.time())
            print("start",(float(time.time())-clock))
            for i in article.findAll('li',class_="news-card horizontal-lead col4 news"):
                
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('span',class_='con_wrap').text
                t = Translator()
                PostHeading = t.translate(PostHeading,src='te',dest='en').text
                print(PostHeading)
                try:
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            GatherDataSamayam19(i,d,subdict,PostHeading)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        GatherDataSamayam19(i,d,subdict,PostHeading)
                except Exception as e:
                    print(e)
                    continue
            if flag==1:
                break
            c+=1
        print(len(subdict),"artiles updated in from indiatoday")  
            #reversing the dict for restoring the order
        #subdict=OrderedDict(reversed(list(subdict.items())))
            #picle me dictionary store kr rahe  hai
        write_to_file19(subdict)
    except:
        pass
def GatherTheHansIndia19(i,d,subdict,PostHeading):
    try:
        # andre wali post ka url
        PostUrl = "https://www.thehansindia.com"+i.find('a')['href']
        print(PostUrl)
        # post image ka url
        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostImageAddress=Postsoup.find('div',class_='image-wrap').find('img')['src']
        print(PostImageAddress)
        PostArticle=Postsoup.find('div',class_='relative-position')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            
            if len(j.text)>4:
                PostComplete+=j.text
        Summary=Shorten19(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
        print(PostImageAddress)
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeTheHansIndia19(d,isNewsPickle):
    try:
        c=1
        # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
        subdict=OrderedDict()
        #reprocessing se bachane k liye
        flag=0
        count=0   
        while(c<3):
            URL = "https://www.thehansindia.com/andhra-pradesh/"+str(c)
            r = requests.get(URL).text
            soup = BeautifulSoup(r, 'lxml')
            article=soup.find('div',class_='row two-colum-listing bigger-image')
            count=0
            clock=float(time.time())
            print("start",(float(time.time())-clock))
            for i in article.findAll('div',class_='col-md-6'):

                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('div',class_='col-md-8 col-8').find('a').text
                try:
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            GatherTheHansIndia19(i,d,subdict,PostHeading)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        GatherTheHansIndia19(i,d,subdict,PostHeading)
                except Exception as e:
                    print(e)
                    continue
            if flag==1:
                break
            c+=1
        print(len(subdict),"artiles updated in from indiatoday")  
            #reversing the dict for restoring the order
        #subdict=OrderedDict(reversed(list(subdict.items())))
            #picle me dictionary store kr rahe  hai
        write_to_file19(subdict)
    except:
        pass
def ScrapSuper19(i,d,isNewsPickle):
    if i==0:
        ScrapeGreatAndhra19(d,isNewsPickle)
    elif i==1:
        ScrapeTheHansIndia19(d,isNewsPickle)
    if i==2:
        ScrapeSamayam19(d,isNewsPickle)
def scrape_state_andhrapradesh_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper19, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData19))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData19.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'andhrapradesh', None], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData19.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#       END ANDHRAPRADESH NEWS SCRAPER                  #
#                                                       #
#########################################################



#########################################################
#                                                       #
#       START RAJASTHAN NEWS SCRAPER                    #
#                                                       #
#########################################################



ScrapedData21 = dict()
def write_to_file21(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData21.update(subdict)
    global_lock.release()
def Shorten21(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataLiveHindustan21(i,d,subdict):
    try:
        PostUrl ="https://www.livehindustan.com"+i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        translator = Translator()
        PostHeading = translator.translate(PostHeading,src='hi',dest='en').text
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='story-page-content')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='carousel-inner story-page-inner carousel-Sec story-detail-img').find('img')['data-src']
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten21(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeLiveHindustan21(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<5):
        URL = "https://www.livehindustan.com/rajasthan/news-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='right-top-news no-pad personality-celebrity listing-widgets-content')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                translator = Translator()
                PostHeading= translator.translate(PostHeading,src='hi',dest='en').text
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataLiveHindustan21(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveHindustan21(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file21(subdict)
def GatherDataHindustanTimes21(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='storyDetail')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten21(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeHindustanTimes21(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<5):
        URL = "https://www.hindustantimes.com/topic/rajasthan/page-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='mainContent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="authorListing"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes21(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes21(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file21(subdict)
def GatherDataZeeNews21(i,d,subdict):
    try:
        PostUrl ="https://zeenews.india.com"+i.find('a')['href']
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='article-right-col main')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='article-image-block margin-bt30px').find('img')['src']
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten21(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeZeeNews21(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    while(c<2):
        URL = "https://zeenews.india.com/rajasthan"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',class_='maincontent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="section-article margin-bt30px clearfix"):
            try:
                if c>=60:
                    break
                c+=1
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataZeeNews21(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews21(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file21(subdict)
def ScrapSuper21(i,d,isNewsPickle):
    if i==0:
        ScrapeLiveHindustan21(d,isNewsPickle)
    elif i==1:
        ScrapeZeeNews21(d,isNewsPickle)
    elif i==2:
        ScrapeHindustanTimes21(d,isNewsPickle)
def scrape_state_rajasthan_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper21, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData21))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData21.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'rajasthan', None], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData21.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#           END RAJASTHAN NEWS SCRAPER                  #
#                                                       #
#########################################################



#########################################################
#                                                       #
#          START UTTAR PRADESH NEWS SCRAPER             #
#                                                       #
#########################################################


ScrapedData4 = dict()
def write_to_file4(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData4.update(subdict)
    global_lock.release()
def Shorten4(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataJagran4(i, d, subdict, PostHeading, translator):
    try:
        # andre wali post ka url
        PostUrl = "https://www.jagran.com"+i.find('a')['href']
        # post image ka url
        PostImageAddress = i.find('img')['data-src']
        if not PostImageAddress.startswith('http'):
                PostImageAddress = "https:" + i.find('img')['data-src']
        # post ki heading
        # PostHeading = i.find('h3').text

        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle = Postsoup.find('div', class_='articleBody')
        PostComplete = ""
        for j in PostArticle.findAll('p'):
            PostComplete += j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete, src='hi', dest='en').text
        Summary = Shorten4(PostComplete, PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary) > 1:
            subdict[PostHeading] = [
                PostUrl, PostImageAddress, PostHeading, Summary]
    except:
        print("iss mai error aaya-->",PostHeading)
def ScrapeJagran4(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://www.jagran.com/topics/uttar-pradesh-p"+str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('ul', class_='topicList')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('h3').text
                PostHeading = translator.translate(
                    PostHeading, src='hi', dest='en').text

                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataJagran4(i, d, subdict, PostHeading, translator)
                    else:
                        flag = 1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran4(i, d, subdict, PostHeading, translator)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Jagran")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file4(subdict)
def GatherDataLiveHindustan4(i, d, subdict, PostHeading, translator):
    PostUrl = "https://www.livehindustan.com"+i.find('a')['href']
    print(PostUrl)
    # PostHeading = i.find('img')['title']
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PostUrl, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('div', class_='story-page-content')
    PostComplete = ""
    for j in article.findAll('p'):
        PostComplete += j.text
    PostImageAddress = soup.find(
        'div', class_='carousel-inner story-page-inner carousel-Sec story-detail-img').find('img')['data-src']
    translator = Translator()
    PostComplete = translator.translate(PostComplete, src='hi', dest='en').text
    Summary = Shorten4(PostComplete, PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary) > 1:
        subdict[PostHeading] = [
            PostUrl, PostImageAddress, PostHeading, Summary]
def ScrapeLiveHindustan4(d, isNewsPickle):
    translator = Translator()
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 5):
        URL = "https://www.livehindustan.com/uttar-pradesh/news-"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find(
            'ul', class_='right-top-news no-pad personality-celebrity listing-widgets-content')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                PostHeading = translator.translate(
                    PostHeading, src='hi', dest='en').text
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataLiveHindustan4(i, d, subdict, PostHeading, translator)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveHindustan4(i, d, subdict, PostHeading, translator)
            except:
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Live Hindustan")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file4(subdict)
def GatherDataZeeNews4(i, d, subdict):

    PostUrl = "https://zeenews.india.com"+i.find('a')['href']
    PostHeading = i.find('img')['title']
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PostUrl, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('div', class_='article-right-col main')
    PostComplete = ""
    for j in article.findAll('p'):
        PostComplete += j.text
    PostImageAddress = soup.find(
        'div', class_='article-image-block margin-bt30px').find('img')['src']
    Summary = Shorten4(PostComplete, PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary) > 1:
        subdict[PostHeading] = [
            PostUrl, PostImageAddress, PostHeading, Summary]
def ScrapeZeeNews4(d, isNewsPickle):
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        URL = "https://zeenews.india.com/tags/uttar-pradesh.html-"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('section', class_='maincontent')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('div', class_="section-article margin-bt30px clearfix"):
            try:
                if c >= 60:
                    break
                c += 1
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['title']
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataZeeNews4(i, d, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews4(i, d, subdict)
            except Exception as e:
                print(e)
                continue
        c += 1
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Zee News")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file4(subdict)
def ScrapSuper4(i, d, isNewsPickle):
    if i == 0:
        ScrapeJagran4(d, isNewsPickle)
    elif i == 1:
        ScrapeLiveHindustan4(d, isNewsPickle)
    if i == 2:
        ScrapeZeeNews4(d, isNewsPickle)
def scrape_state_uttarpradesh_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper4, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData4))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData4.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'uttarpradesh', None], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData4.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#           END UTTAR PRADESH NEWS SCRAPER              #
#                                                       #
#########################################################



#########################################################
#                                                       #
#               START TECH NEWS SCRAPER                 #
#                                                       #
#########################################################



ScrapedData5 = dict()
def write_to_file5(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData5.update(subdict)
    global_lock.release()
def Shorten5(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataLiveMint5(i, d, subdict):
    PostUrl = "https://www.livemint.com"+i.find('a')['href']
    print(PostUrl)
    PostHeading = i.find('img')['title']
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PostUrl, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('section', class_="mainSec")
    PostComplete = ""
    for j in article.findAll('p'):
        PostComplete += j.text
    PostImageAddress = soup.find(
        'figure').find('img')['alt']
    Summary = Shorten5(PostComplete, PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary) > 1:
        subdict[PostHeading] = [
            PostUrl, PostImageAddress, PostHeading, Summary]
def ScrapeLiveMint5(d, isNewsPickle):
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 2):
        URL = "https://www.livemint.com/technology/tech-news"
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='listView')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('div', class_="listing clearfix impression-candidate"):
            try:
                print(1)
                if c >= 60:
                    break
                if(not i.find('img')):
                    continue
                value = (float(time.time())-clock)
                print(count, value)
                count += 1
                PostHeading = i.find('img')['alt']
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataLiveMint5(i, d, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveMint5(i, d, subdict)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Live Mint")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file5(subdict)
def GatherDataGadgetsNow5(i, d, PostHeading, subdict):
    PostUrl = "https://www.gadgetsnow.com"+i.find('a')['href']
    print(PostUrl)
    # PostHeading=i.find('img')['alt']
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PostUrl, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    # article = soup.find('div', class_="data")
    PostComplete = soup.find('div', class_="Normal").text
    PostImageAddress = soup.find(
        'div', class_='highlight_img').find('img')['src']
    Summary = Shorten5(PostComplete,PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary) > 1:
        subdict[PostHeading] = [
            PostUrl, PostImageAddress, PostHeading, Summary]
def ScrapeGadgetsNow5(d, isNewsPickle):
    c = 1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        if c == 1:
            URL = "https://www.gadgetsnow.com/tech-news"
        else:
            URL = "https://www.gadgetsnow.com/tech-news/"+str(c)
        print(URL)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='tech_list ctn_stories')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            if c >= 60:
                break
            if(not i.find('img')):
                continue
            value = (float(time.time())-clock)
            print(count, value)
            count += 1

            PostHeading = i.find('span', class_='w_tle').text
            try:
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataGadgetsNow5(i, d, PostHeading, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataGadgetsNow5(i, d, PostHeading, subdict)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Gadgets Now")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file5(subdict)
def GatherDataGadgetsNdtv5(i, d, PostHeading, subdict):
    # global gn
    PostUrl = i.find('a')['href']
    print(PostUrl)
    # PostHeading=i.find('img')['alt']
    agent = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PostUrl, headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('div', class_="content_text row description")
    PostComplete = ""
    for j in article.findAll('p'):
        PostComplete += j.text
    PostImageAddress = soup.find(
        'div', class_='fullstoryImage').find('img')['src']
    Summary = Shorten5(PostComplete, PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary) > 1:
        subdict[PostHeading] = [
            PostUrl, PostImageAddress, PostHeading, Summary]
def ScrapeGadgetsNdtv5(d, isNewsPickle):
    # page 2 se start kar ra
    c = 0
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict = OrderedDict()
    # reprocessing se bachane k liye
    flag = 0
    count = 0
    while(c < 4):
        # if c==1:
        URL = "https://gadgets.ndtv.com/news/page-"+str(c)
        agent = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('div', class_='story_list row margin_b30')
        count = 0
        clock = float(time.time())
        print("start", (float(time.time())-clock))
        for i in article.findAll('li'):
            if c >= 60:
                break
            if(not i.find('img')):
                continue
            value = (float(time.time())-clock)
            print(count, value)
            count += 1
            PostHeading = i.find('span', class_='news_listing').text
            try:
                if isNewsPickle == 1:
                    if PostHeading not in d:
                        GatherDataGadgetsNdtv5(i, d, PostHeading, subdict)
                    else:
                        flag = 1
                        print(
                            "----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataGadgetsNdtv5(i, d, PostHeading, subdict)
            except Exception as e:
                print(e)
                continue
        if flag == 1:
            break
        c += 1
    print(len(subdict), "artiles updated in from Gadgets Ndtv")
    # reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    # picle me dictionary store kr rahe  hai
    write_to_file5(subdict)
def ScrapSuper5(i, d, isNewsPickle):
    if i == 0:
        ScrapeLiveMint5(d, isNewsPickle)
    elif i == 1:
        ScrapeGadgetsNdtv5(d, isNewsPickle)
    elif i == 2:
        ScrapeGadgetsNow5(d, isNewsPickle)
def scrape_tech_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(5):
            p = threading.Thread(target=ScrapSuper5, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData5))
        post_data = {"news_type": "tech_news", "news": []}
        for data in ScrapedData5.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(
                data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData5.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#                END TECH NEWS SCRAPER                  #
#                                                       #
#########################################################



#########################################################
#                                                       #
#           START UP DISTRICT NEWS SCRAPER              #
#                                                       #
#########################################################



ScrapedData6 = dict()
def write_to_file6(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData6.update(subdict)
    global_lock.release()
def Shorten6(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataLiveHindustan6(i,d,subdict,dist,PostHeading, translator):
    try:
        PostUrl ="https://www.livehindustan.com"+i.find('a')['href']
        print(PostUrl)
        #PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='story-page-content')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='carousel-inner story-page-inner carousel-Sec story-detail-img').find('img')['data-src']
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten6(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest="en")
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]
        print(PostHeading)
    except:
        print("iss mai error aaya -->",PostHeading)
def ScrapeLiveHindustan6(d,isNewsPickle,dist):
    translator = Translator()
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<2):
        URL = "https://www.livehindustan.com/uttar-pradesh/"+dist+"/news-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='right-top-news no-pad personality-celebrity listing-widgets-content')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                PostHeading=translator.translate(PostHeading,src="hi",dest='en').text
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataLiveHindustan6(i,d,subdict,dist,PostHeading, translator)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveHindustan6(i,d,subdict,dist,PostHeading, translator)
            except:
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from Live Hindustan")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file6(subdict)
def GatherDataJagran6(i,d,subdict,dist,PostHeading, translator):
    # andre wali post ka url
    PostUrl = "https://english.jagran.com"+i.find('a')['href']
    # post image ka url
    PostImageAddress= str(i.find('img')['data-src'])
    if not PostImageAddress.startswith('http'):
            PostImageAddress = "https:" + str(i.find('img')['data-src'])
    print(PostUrl)
    # post ki heading
     #PostHeading=i.find('h3').text
    
    # post ka content uske url pr jakr extract kr re
    PortReq = requests.get(PostUrl).text
    Postsoup = BeautifulSoup(PortReq, 'lxml')
    PostArticle=Postsoup.find('div',class_='articleBody')
    PostComplete=""
    for j in PostArticle.findAll('p'):
        PostComplete+=j.text
    PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
    Summary=Shorten6(PostComplete,PostHeading)
    t=Translator()
    Summary=t.translate(Summary,dest='en').text
    if len(Summary)>1:
        subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]
def ScrapeJagran6(d,isNewsPickle,dist):
    translator = Translator()
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://english.jagran.com/search/"+dist+"-page"+str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):

            value=(float(time.time())-clock)
            print(count,value)
            count+=1
            try:
                PostHeading=i.find('div',class_='h3').text
                PostHeading = translator.translate(PostHeading, src='hi', dest='en').text
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataJagran6(i,d,subdict,dist,PostHeading, translator)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran6(i,d,subdict,dist,PostHeading, translator)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from Jagaran")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file6(subdict)
def GatherDataZeeNews6(i,d,subdict,dist,PostHeading):
        PostUrl ="https://zeenews.india.com"+i.find('a')['href']
        #PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='article-right-col main')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='article-image-block margin-bt30px').find('img')['src']
        # translator = Translator()
        # PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten6(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]
def ScrapeZeeNews6(d,isNewsPickle,dist):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    while(c<4):
        URL = "https://zeenews.india.com/tags/uttar-pradesh.html-"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',class_='maincontent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="section-article margin-bt30px clearfix"):
            try:
                if c>=60:
                    break
                c+=1
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataZeeNews6(i,d,subdict,dist,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews6(i,d,subdict,dist,PostHeading)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from Zee news")  
    #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file6(subdict)
def ScrapSuper6(i,d,isNewsPickle,dist):
    # if i==0:
    #     ScrapeJagran6(d,isNewsPickle,dist)
    if i==1:
        ScrapeLiveHindustan6(d,isNewsPickle,dist)
    # if i==2:
    #     ScrapeZeeNews6(d,isNewsPickle,dist)
def scrape_state_uttarpradesh_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(3):
                p = threading.Thread(target=ScrapSuper6,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData6))
            for data in ScrapedData6.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'uttarpradesh', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData6.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#            END UP DISTRICT NEWS SCRAPER               #
#                                                       #
#########################################################



#########################################################
#                                                       #
#        START KARNATAKA DISTRICT NEWS SCRAPER          #
#                                                       #
#########################################################



ScrapedData7 = dict()
def write_to_file7(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData7.update(subdict)
    global_lock.release()
def Shorten7(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def NewsKarnatakaGatherData7(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='news_detail')
        PostImageAddress="https://www.newskarnataka.com/"+PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten7(PostComplete,PostComplete)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except:
        print("----->isme error aya",PostHeading)
def ScrapNewsKarnataka7(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.newskarnataka.com/"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        try:
            c+=1
            URL =address+city
            agent = {"User-Agent":"Mozilla/5.0"}
            r = requests.get(URL,headers=agent).text
            soup = BeautifulSoup(r, 'lxml')
            article=soup.find('ul',class_='listed_news two_col_list classified_list inner')
            for i in article.findAll('li'):
                try:
                    count+=1
                    PostHeading=i.find('a')['title']
                    PostUrl=i.find('a')['href']
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            NewsKarnatakaGatherData7(i,PostHeading,PostUrl,subdict,city)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        NewsKarnatakaGatherData7(i,PostHeading,PostUrl,subdict,city)
                except:
                    continue
            if flag==1:
                break
        except:
            c+=1
            continue
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file7(subdict)
def PrajavaniGatherData7(i,PostHeading,Url,subdict,dist, translator):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='content')
        PostImageAddress=PostArticle.find('div',class_='field field-name-field-image field-type-image field-label-hidden').find('div',class_='field-items').find('div',class_='field-item even').find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        PostComplete = translator.translate(PostComplete,src='kn',dest='en').text
        Summary=Shorten7(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except:
        print("----->isme error aya",PostHeading)
def ScrapPrajavani7(d,isNewsPickle,dist):
    translator=Translator()
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.prajavani.net"
    #newspicle_pehle_se_hai?
    count=0
    c=0
    while(c<1):
        c+=1
        URL =address+'/'+city
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='group')
        for i in article.findAll('div',class_='pj-top-trending__img-wrapper'):
            count+=1
            PostUrl=address+i.find('a')['href']
            PostHeading=i.find('a').find('img')['alt']
            PostHeading=translator.translate(PostHeading,src='kn',dest='en').text
            if isNewsPickle==1:
                if PostHeading not in d:
                    PrajavaniGatherData7(i,PostHeading,PostUrl,subdict,dist, translator)
                else:
                    flag=1
                    print("----->bas itna hi update hua hai.... baki apne paas already hai")
                    break
            else:
                PrajavaniGatherData7(i,PostHeading,PostUrl,subdict,dist, translator)
        if flag==1:
            break
    print(len(subdict),"artiles updated in from Prajavani in ",city)
    write_to_file7(subdict)
def ScrapSuper7(i,d,isNewsPickle,district):
    prajavance_conversion_dict = {'bangalore': "bengaluru-city", 'mysore': 'mysore', 'udupi': 'udupi', 'shimoga': 'shivamogga', 'belagavi':'belagavi'}
    prajavani_district = prajavance_conversion_dict.get(district, None)
    if i==0 and prajavani_district is not None:
        ScrapPrajavani7(d,isNewsPickle,prajavani_district)
    elif i==1:
        ScrapNewsKarnataka7(d,isNewsPickle,district)
def scrape_state_karnataka_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(2):
                p = threading.Thread(target=ScrapSuper7,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData7))
            for data in ScrapedData7.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'karnataka', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData7.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#          END KARNATAKA DISTRICT NEWS SCRAPER          #
#                                                       #
#########################################################



#########################################################
#                                                       #
#       START WESTBENGAL DISTRICT NEWS SCRAPER          #
#                                                       #
#########################################################



ScrapedData16 = dict()
def write_to_file16(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData16.update(subdict)
    global_lock.release()
def Shorten16(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def SiliguriTimesGatherData16(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',id='content')
        PostImageAddress=PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten16(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,src="mr",dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
            #print("\n\n",PostUrl,"\n",PostImageAddress,'\n',PostHeading,"\n",Summary,"\n")
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapSiliguriTimes16(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://siliguritimes.com/category/"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        URL =address+"/"+city+"/"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='row large-columns-2 medium-columns- small-columns-1 row-masonry')
        for i in article.findAll('div',class_="col post-item"):
            try:
                count+=1
                PostHeading=i.find('h5').text
                PostUrl=i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        SiliguriTimesGatherData16(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    SiliguriTimesGatherData16(i,PostHeading,PostUrl,subdict,city)
            except:
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file16(subdict)
def GatherDataTelegraphIndia16(i,d,subdict,post):
    try:
        PostUrl ="https://www.telegraphindia.com"+i.find('a')['href']
        print(PostUrl)
        PostHeading=post
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.findAll('div',class_="col-12")[1]
        PostComplete=""
        for j in article.find('div',class_="fs-17 pt-2 noto-regular").findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['src']
        Summary=Shorten16(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,"kolkata"]
    except Exception as e:
        print(e)
def ScrapeTelegraphIndia16(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://www.telegraphindia.com/west-bengal/calcutta/page-"+str(c)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='row uk-grid-divider pb-3')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_='row pb-3 pt-3'):
            try:
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h2').text
                PostHeading=PostHeading.replace(" ","")
                PostHeading=PostHeading.replace("\n","")
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataTelegraphIndia16(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataTelegraphIndia16(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file16(subdict)
def GatherDataJagran16(i,Post,d,subdict,city):
    # andre wali post ka url
    try:
        PostUrl = "https://www.jagran.com"+i.find('a')['href']
        # post image ka url
        PostImageAddress="https:"+i.find('img')['data-src']

        # post ki heading
        PostHeading=Post

        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='articleBody')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten16(PostComplete,PostHeading)
        Summary= translator.translate(Summary,src='hi',dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,city]
        print(PostImageAddress)
    except Exception as e:
        print(e)
def ScrapJagran16(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.jagran.com/local/west-bengal_"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<3):
        c+=1
        URL =address+city+"-news-hindi-page"+str(c)+".html"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        for i in article.findAll('li'):
            try:
                count+=1
                PostHeading=i.find('div',class_='h3').text
                print(PostHeading)
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="hi",dest="en").text
                PostUrl=i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataJagran16(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran16(i,PostHeading,PostUrl,subdict,city)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file16(subdict)
def ScrapSuper16(i,d,isNewsPickle,district):
    Siliguri={'alipurduar':'alipurduar','cooch-behar':'cooch-behar','darjeeling':'darjeeling','jalpaiguri':'jalpaiguri','kalimpong':'kalimpong','siliguri':'siliguri'}
    Jagran={'jalpaiguri':"jalpaiguri",'darjeeling':"darjeeling",'cooch-behar':"cooch-behar",'kolkata':"kolkata","purulia":"purulia",'khadagpur':"khadagpur"}
    StDist=Siliguri.get(district,None)
    JDist=Jagran.get(district,None)
    if i==0 and StDist!=None:
        ScrapSiliguriTimes16(d,isNewsPickle,StDist)
    if i==1:
        ScrapeTelegraphIndia16(d,isNewsPickle)
    if i==2 and JDist!=None:
        ScrapJagran16(d,isNewsPickle,JDist)
def scrape_state_westbengal_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(3):
                p = threading.Thread(target=ScrapSuper16,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData16))
            for data in ScrapedData16.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'westbengal', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData16.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#          END WESTBENGAL DISTRICT NEWS SCRAPER         #
#                                                       #
#########################################################



#########################################################
#                                                       #
#          START GUJARAT DISTRICT NEWS SCRAPER          #
#                                                       #
#########################################################


ScrapedData18 = dict()
def write_to_file18(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData18.update(subdict)
    global_lock.release()
def Shorten18(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def SandeshGatherData18(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',id='content-area')
        try:
            PostImageAddress=PostArticle.find('img')['src']
        except:
            PostImageAddress="https://www.elegantthemes.com/blog/wp-content/uploads/2019/10/loading-screen-featured-image.jpg"
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        t=Translator()
        PostComplete=t.translate(PostComplete,src='gu',dest='en').text
        Summary=Shorten18(PostComplete,PostHeading)
        Summary=t.translate(Summary,dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapSandesh18(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="http://sandesh.com/category"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        URL =address+"/"+city+"/page/"+str(c)+"/"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',id='content-area')
        for i in article.findAll('div',class_="et_pb_column et_pb_column_1_3 d-s-paddingR20"):
            try:
                count+=1
                PostHeading=i.find('p',class_="d-s-trend-news-content d-s-NSG-regular").text
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="gu",dest="en").text
                print(PostHeading)
                PostUrl=i.find('p',class_="d-s-trend-news-content d-s-NSG-regular").find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        SandeshGatherData18(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    SandeshGatherData18(i,PostHeading,PostUrl,subdict,city)
            except:
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file18(subdict)
def JagranGatherData18(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostImageAddress="https:"+i.find('img')['data-src']
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='articleBody')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten18(PostComplete,PostComplete)
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
        print(PostImageAddress)

    except:
        print("----->isme error aya",PostHeading)
def ScrapJagran18(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.jagran.com/local/gujarat_"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        URL =address+city+"-news-hindi-page"+str(c)+".html"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        for i in article.findAll("li"):
            try:
                count+=1
                PostHeading=i.find('div',class_='h3').text
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="gu",dest="en").text
                print(PostHeading)
                PostUrl="https://www.jagran.com"+i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        JagranGatherData18(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    JagranGatherData18(i,PostHeading,PostUrl,subdict,city)
            except:
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file18(subdict)
def ScrapSuper18(i,d,isNewsPickle,j):
    Sandesh_Dict={'ahmedabad':'ahmedabad','baroda':'baroda','bhavnagar':'bhavnagar','kutch-bhuj':'kutch-bhuj','rajkot':'rajkot','surat':'surat','patna-banaskantha':'patan-banaskantha','mehsana':'mehsana'}
    Jagran_Dict={'ahmedabad':'ahmedabad','vadodara':'vadodara','surat':'surat'}
    Sandesh=Sandesh_Dict.get(j,None)
    Jagran=Jagran_Dict.get(j,None)
    if i==0 and Sandesh!=None:
        ScrapSandesh18(d,isNewsPickle,Sandesh)
    if i==1 and Jagran!=None :
        ScrapJagran18(d,isNewsPickle,Jagran)
def scrape_state_gujarat_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(3):
                p = threading.Thread(target=ScrapSuper18,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData18))
            for data in ScrapedData18.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'gujarat', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData18.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#          END GUJARAT DISTRICT NEWS SCRAPER            #
#                                                       #
#########################################################



#########################################################
#                                                       #
#       START ANDHRAPRADESH DISTRICT NEWS SCRAPER       #
#                                                       #
#########################################################



ScrapedData20 = dict()
def write_to_file20(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData20.update(subdict)
    global_lock.release()
def Shorten20(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataSakshi20(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='field-item even')
        PostImageAddress=Postsoup.find('img',class_="unveil")['data-src'].split(".jpg")[0]+".jpg"
        print(PostImageAddress)
        PostArticle=Postsoup.find('p',class_='rtejustify')
        PostComplete=PostArticle.text
        t=Translator()
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        PostComplete= t.translate(PostComplete,src='te',dest='en').text
        Summary=Shorten20(PostComplete,PostHeading)
        Summary=t.translate(Summary,dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except:
        print("----->isme error aya",PostHeading)
def ScrapSakshi20(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.sakshi.com/"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        try:
            c+=1
            URL =address+"andhra-pradesh/"+city
            print(URL)
            agent = {"User-Agent":"Mozilla/5.0"}
            r = requests.get(URL,headers=agent).text
            soup = BeautifulSoup(r, 'lxml')
            article=soup.find('div',id='block-system-main').find('div',class_='view-content')
            for j in range(1,30):
                try:
                    if j==1:
                        i=article.find('div',class_='views-row views-row-'+str(j)+' views-row-odd views-row-first rowarticle')
                    elif j%2!=0:
                        i=article.find('div',class_='views-row views-row-'+str(j)+' views-row-odd rowarticle')
                    else:
                        i=article.find('div',class_='views-row views-row-'+str(j)+' views-row-even rowarticle')
                    count+=1
                    PostHeading=i.find('span',class_='field-content').text
                    translator=Translator()
                    PostHeading=translator.translate(PostHeading,src="te",dest="en").text
                    print(PostHeading)
                    PostUrl=address+i.find('a')['href']
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            GatherDataSakshi20(i,PostHeading,PostUrl,subdict,city)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        GatherDataSakshi20(i,PostHeading,PostUrl,subdict,city)
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file20(subdict)
def ScrapSuper20(i,d,isNewsPickle,j):
    if i==0:
        ScrapSakshi20(d,isNewsPickle,j)
def scrape_state_andhrapradesh_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(3):
                p = threading.Thread(target=ScrapSuper20,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData20))
            for data in ScrapedData20.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'andhrapradesh', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData20.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#          END ANDHRAPRADESH DISTRICT NEWS SCRAPER      #
#                                                       #
#########################################################



#########################################################
#                                                       #
#          START RAJASTHAN DISTRICT NEWS SCRAPER        #
#                                                       #
#########################################################



ScrapedData22 = dict()
def write_to_file22(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData22.update(subdict)
    global_lock.release()
def Shorten22(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def DainikNavaJyotiGatherData22(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.findAll('div',class_='row_width')[4]
        PostImageAddress="https://www.dainiknavajyoti.net"+PostArticle.find('img',class_='adjimage1')['src']
        print(PostImageAddress)
        PostComplete=""
    #         for j in PostArticle.findAll('p'):
        PostComplete+=PostArticle.find('div',id='contentsec').find('p').text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        t=Translator()
        PostComplete=t.translate(PostComplete,src="hi",dest="en").text
        print(PostComplete)
        Summary=Shorten22(PostComplete,PostHeading)
        translator = Translator()
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    #             print("\n\n",PostUrl,"\n",PostImageAddress,'\n',PostHeading,"\n",Summary,"\n")
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapDainikNavaJyoti22(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.dainiknavajyoti.net/"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<4):
        c+=1
        URL =address+city+"/page"+str(c)+".html"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',id='sectiondetail')
        for i in article.findAll('div',class_="section_news"):
            try:
                count+=1
                PostHeading=i.find('h3').text
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="hi",dest="en").text
                PostUrl=i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        DainikNavaJyotiGatherData22(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    DainikNavaJyotiGatherData22(i,PostHeading,PostUrl,subdict,city)
            except Exception as e:
                print(e)
                break
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file22(subdict)
def GatherDataZeeNews22(i,d,subdict,dist,PostHeading):
    try:
        PostUrl ="https://zeenews.india.com"+i.find('a')['href']
        #PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='article-right-col main')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='article-image-block margin-bt30px').find('img')['src']
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten22(PostComplete,PostHeading)
        translator = Translator()
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeZeeNews22(d,isNewsPickle,dist):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    address="https://zeenews.india.com/hindi/india/rajasthan/"
    while(c<2):
        URL =address + dist
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',class_='maincontent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="section-article margin-bt30px clearfix"):
            try:
                if c>=60:
                    break
                c+=1
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataZeeNews22(i,d,subdict,dist,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews22(i,d,subdict,dist,PostHeading)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in",dist)  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file22(subdict)
def GatherDataDainikJalteDeep22(i,d,subdict,dist,PostHeading):
    try:
        PostUrl =i.find('a')['href']
        #PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='td-post-content')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_='td-post-featured-image').find('img')['src']
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        print(PostComplete)
        Summary=Shorten22(PostComplete,PostHeading)
        translator = Translator()
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]

    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeDainikJalteDeep22(d,isNewsPickle,dist):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    address="https://dainikjaltedeep.com/state/"
    while(c<2):
        URL =address + dist
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='td-big-grid-scroll')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        l=1
        while(l<5):
            i =article.find('div',class_="td_module_mx6 td-animation-stack td-meta-info-hide td-big-grid-post-"+str(l)+" td-big-grid-post td-small-thumb")
            l+=1
            try:
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataDainikJalteDeep22(i,d,subdict,dist,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataDainikJalteDeep22(i,d,subdict,dist,PostHeading)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
    c=0
    while(c<2):
        URL =address + dist
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='td-ss-main-content')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="td-block-span4"):
            try:
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataDainikJalteDeep22(i,d,subdict,dist,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataDainikJalteDeep22(i,d,subdict,dist,PostHeading)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in",dist)  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file22(subdict)
def ScrapSuper22(i,d,isNewsPickle,j):
    li=['jaipur','jodhpur','kota','udaipur','bikaner','ajmer','bharatpur','sri-ganganagar','jaisalmer','jhunjhunu','churu','alwar','dungarpur','bhilwara','chittorgarh']
    li2=['jaipur','jodhpur','kota','udaipur','bikaner','ajmer','bharatpur']
    if i==0 and j in li:
        ScrapeDainikJalteDeep22(d,isNewsPickle,j)
    elif i==1 and j in li2:
        ScrapeZeeNews22(d,isNewsPickle,j)
    elif i==2 and j in li:
        ScrapDainikNavaJyoti22(d,isNewsPickle,j)
def scrape_state_rajasthan_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(3):
                p = threading.Thread(target=ScrapSuper22,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData22))
            for data in ScrapedData22.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'rajasthan', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData22.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#          END RAJASTHAN DISTRICT NEWS SCRAPER          #
#                                                       #
#########################################################



#########################################################
#                                                       #
#                START DELHI NEWS SCRAPER               #
#                                                       #
#########################################################



ScrapedData8 = dict()
def write_to_file8(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData8.update(subdict)
    global_lock.release()
def Shorten8(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def HindustanTimesGatherData8(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='mainContent')
        PostImageAddress="https://www.newskarnataka.com/"+PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.find('div',class_='storyDetail').findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten8(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapHindustanTimes8(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    URL="https://www.hindustantimes.com/delhi-news/"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='latest-news-bx row')
        for i in article.findAll('li'):
            try:
                count+=1
                PostHeading=i.find('div','media-img').find('a')['title']
                PostUrl=i.find('div','media-img').find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        HindustanTimesGatherData8(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    HindustanTimesGatherData8(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    c=1
    a="latest-news-morenews more-latest-news more-separate newslist-sec"
    while(c<5):
        if c!=1:
            URL="https://www.hindustantimes.com/delhi-news/page/?pageno="+str(c)
            a="latest-news-bx more-latest-news more-separate"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_=a)
        for i in article.findAll('li'):
            try:
                count+=1
                PostHeading=i.find('div','media-left').find('a')['title']
                PostUrl=i.find('div','media-left').find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        HindustanTimesGatherData8(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    HindustanTimesGatherData8(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    
    print(len(subdict),"artiles updated in from hindustan times in ")
    write_to_file8(subdict)
def IndianExpressGatherData8(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='main-story')
        PostImageAddress=PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        # translator=Translator()
        Summary=Shorten8(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapIndianExpress8(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://indianexpress.com/section/cities/delhi/"
    #newspicle_pehle_se_hai?
    count=0
    c=0
    while(c<1):
        URL=address
        c+=1
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='cities-stories')
        for i in article.findAll('div',class_='story'):
            try:
                count+=1
                PostUrl=i.find('a')['href']
                PostHeading=i.find('img')['alt']
                # translator=Translator()
                if isNewsPickle==1:
                    if PostHeading not in d:
                        IndianExpressGatherData8(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    IndianExpressGatherData8(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from indian express in ")
    write_to_file8(subdict)
def ScrapSuper8(i,d,isNewsPickle):
    if i==0 :
        ScrapIndianExpress8(d,isNewsPickle)
    if i==1:
        ScrapHindustanTimes8(d,isNewsPickle)
def scrape_state_delhi_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(2):
            p = threading.Thread(target=ScrapSuper8, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData8))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData8.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'delhi', None], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData8.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#                 END DELHI NEWS SCRAPER                #
#                                                       #
#########################################################



#########################################################
#                                                       #
#            START MAHARASHTRA NEWS SCRAPER             #
#                                                       #
#########################################################



ScrapedData9 = dict()
def write_to_file9(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData9.update(subdict)
    global_lock.release()
def Shorten9(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def HindustanTimesGatherData9(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='mainContent')
        PostImageAddress="https://www.newskarnataka.com/"+PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.find('div',class_='storyDetail').findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten9(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapHindustanTimes9(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    URL="https://www.hindustantimes.com/topic/maharashtra/page-"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<4):
        c+=1
        URL+=str(c)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='mainContent')
        for i in article.findAll('div',class_="authorListing"):
            try:
                count+=1
                PostHeading=i.find('div','media-img').find('a')['title']
                PostUrl=i.find('div','media-img').find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        HindustanTimesGatherData9(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    HindustanTimesGatherData9(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    c=1
    print(len(subdict),"artiles updated in from hindustan times in ")
    write_to_file9(subdict)
def ZeeNewsGatherData9(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='left-block')
        PostImageAddress=PostArticle.find('div',class_='field-item even').find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        # translator=Translator()
        Summary=Shorten9(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,src="mr",dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapZeeNews9(d,isNewsPickle):
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://zeenews.india.com/marathi/maharashtra"
    #newspicle_pehle_se_hai?
    count=0
    c=0
    while(c<1):
        URL=address
        c+=1
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',class_='maincontent')
        for i in article.findAll('div',class_="section-article margin-bt30px clearfix"):
            try:
                count+=1
                PostUrl="https://zeenews.india.com"+i.find('a')['href']
                PostHeading=i.find('img')['title']
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="mr",dest="en").text
                if isNewsPickle==1:
                    if PostHeading not in d:
                        ZeeNewsGatherData9(i,PostHeading,PostUrl,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    ZeeNewsGatherData9(i,PostHeading,PostUrl,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ")
    write_to_file9(subdict)
def DeccanHeraldGatherData9(i,PostHeading,Url,subdict):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='content')
        PostImageAddress=PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        # translator=Translator()
        Summary=Shorten9(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,src="mr",dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except Exception as e:
        print(e)
        print("----->isme error aya",PostHeading)
def ScrapDeccanHerald9(d,isNewsPickle):
    print(1)
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.deccanherald.com/tag/maharashtra"
    #newspicle_pehle_se_hai?
    count=0
    c=0
    while(c<1):
        URL=address
        c+=1
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.findAll('ul',class_='sm-hr-card-list')
        for j in article:
            for i in j.findAll('li'):
                try:
                    count+=1
                    PostUrl="https://www.deccanherald.com/"+i.find('a')['href']
                    PostHeading=i.find('img')['title']
                    # translator=Translator()
                    #PostHeading=translator.translate(PostHeading,src="mr",dest="en").text
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            DeccanHeraldGatherData9(i,PostHeading,PostUrl,subdict)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        DeccanHeraldGatherData9(i,PostHeading,PostUrl,subdict)
                except Exception as e:
                    print(e)
                    continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from deccan herald in ")
    write_to_file9(subdict)
def ScrapSuper9(i,d,isNewsPickle):
    if i==0 :
        ScrapZeeNews9(d,isNewsPickle)
    if i==1:
        ScrapHindustanTimes9(d,isNewsPickle)
    if i==2:
        ScrapDeccanHerald9(d,isNewsPickle)
def scrape_state_maharashtra_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper9, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData9))
        post_data = {"news_type": "state_news", "news": []}
        for data in ScrapedData9.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'maharashtra', None], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData9.clear()
        time.sleep(1800)




#########################################################
#                                                       #
#              END MAHARASHTRA NEWS SCRAPER             #
#                                                       #
#########################################################



#########################################################
#                                                       #
#       START MAHARASHTRA DISTRICT NEWS SCRAPER         #
#                                                       #
#########################################################



ScrapedData10 = dict()
def write_to_file10(subdict):
    while global_lock.locked():
        continue

    global_lock.acquire()
    ScrapedData10.update(subdict)
    global_lock.release()
def Shorten10(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def LokmatGatherData10(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('section',class_='article-body')
        PostImageAddress=PostArticle.find('img')['src']
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten10(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,src="mr",dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except:
        print("----->isme error aya",PostHeading)
def ScrapLokmat10(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    address="https://www.lokmat.com"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<5):
        c+=1
        URL =address+"/"+city+"/page/"+str(c)+"/"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('aside',class_='lk-leftwrap')
        for i in article.findAll('section',class_="multiple-story"):
            try:
                count+=1
                PostHeading=i.find('img')['title'].split("-")[0]
                translator=Translator()
                PostHeading=translator.translate(PostHeading,src="mr",dest="en").text
                PostUrl=address+i.find('a')['href']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        LokmatGatherData10(i,PostHeading,PostUrl,subdict,city)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    LokmatGatherData10(i,PostHeading,PostUrl,subdict,city)
            except:
                continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from Lokmat in ",city)
    write_to_file10(subdict)
def MaharashtraTimesGatherData10(i,PostHeading,Url,subdict,dist):
    try:
        # andre wali post ka url
        PostUrl=Url
        agent = {"User-Agent":"Mozilla/5.0"}
        PortReq = requests.get(PostUrl,headers=agent).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='story-article')
        PostImageAddress=PostArticle.find('img')['src']
        PostComplete=""
        #for j in PostArticle.findAll('p'):
        #print(PostArticle)
        PostComplete+=PostArticle.find('article',class_="story-content").text
        PostComplete = PostComplete.replace("\n","").replace('.','. ')
        Summary=Shorten10(PostComplete,PostHeading)
        t=Translator()
        Summary=t.translate(Summary,src="mr",dest="en").text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary,dist]  
    except:
        print("----->isme error aya",PostHeading)
def ScrapMaharashtraTimes10(d,isNewsPickle,dist):
    city=dist
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    #address_news
    URL="https://maharashtratimes.com/maharashtra/"+city+"-news/articlelist/2429656.cms?curpg=5"
    #newspicle_pehle_se_hai?
    c=0
    count=0
    while(c<1):
        c+=1
        #URL =address+"/"+city+"/page/"+str(c)+"/"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.findAll('ul',class_='col12 pd0 medium_listing')
        for j in article:
            for i in j.findAll("li"):
                try:
                    count+=1
                    PostHeading=i.find('img')['title']
                    translator=Translator()
                    PostHeading=translator.translate(PostHeading,src="mr",dest="en").text
                    PostUrl=i.find('a')['href']
                    if isNewsPickle==1:
                        if PostHeading not in d:
                            MaharashtraTimesGatherData10(i,PostHeading,PostUrl,subdict,city)
                        else:
                            flag=1
                            print("----->bas itna hi update hua hai.... baki apne paas already hai")
                            break
                    else:
                        MaharashtraTimesGatherData10(i,PostHeading,PostUrl,subdict,city)
                except:
                    continue
        if flag==1:
            break
    print(len(subdict),"artiles updated in from newskarnataka in ",city)
    write_to_file10(subdict)
def ScrapSuper10(i,d,isNewsPickle,j):
    lokmat_conversion_dict = {'mumbai':'mumbai', 'pune': 'pune', 'nagpur': 'nagpur', 'aurangabad': 'aurangabad', 'nashik': 'nashik', 'solapur':'solapur', 'kolhapur': 'kolhapur', 'thane': 'thane', 'ratnagiri': 'ratnagiri'}
    maharashtra_times_conversion_dict = {'mumbai':'mumbai', 'pune': 'pune', 'nagpur': 'nagpur', 'aurangabad': 'aurangabad', 'nashik': 'nashik', 'jalgaon':'jalgaon', 'kolhapur': 'kolhapur', 'thane': 'thane', 'ahmednagar': 'ahmednagar'}
    lokmat_district = lokmat_conversion_dict.get(j, None)
    maharashtra_times_district = maharashtra_times_conversion_dict.get(j, None)

    if i==0 and lokmat_district is not None:
        ScrapLokmat10(d,isNewsPickle,lokmat_district)
    if i==1 and maharashtra_times_district is not None:
        ScrapMaharashtraTimes10(d,isNewsPickle, maharashtra_times_district)
def scrape_state_maharashtra_district_news(languages, pickle_file, districts):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        post_data = {"news_type": "state_news", "news": []}
        for j in districts:
            threads = []
            for i in range(2):
                p = threading.Thread(target=ScrapSuper10,args=(i,d,1,j,))
                threads.append(p)
                p.start()
            [thread.join() for thread in threads]
            print("done")
            print(len(ScrapedData10))
            for data in ScrapedData10.values():
                post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0], 'maharashtra', j], "others": [[i, (translator.translate(
                    data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
                d.append(data[2])
            ScrapedData10.clear()
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        time.sleep(1800)



#########################################################
#                                                       #
#         END MAHARASHTRA DISTRICT NEWS SCRAPER         #
#                                                       #
#########################################################



#########################################################
#                                                       #
#              START TRENDING NEWS SCRAPER              #
#                                                       #
#########################################################



ScrapedData11 = dict()
def write_to_file11(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData11.update(subdict)
    global_lock.release()
def Shorten11(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataLiveMint11(i,d,subdict):
    PostUrl ="https://www.livemint.com"+i.find('a')['href']
    print(PostUrl)
    PostHeading=i.find('img')['title']
    agent = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(PostUrl,headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article=soup.find('section',class_="mainSec")
    PostComplete=""
    for j in article.findAll('p'):
        PostComplete+=j.text
    PostImageAddress=soup.find('section',class_='cardHolder open').find('img')['alt']
    Summary=summarize(PostComplete,word_count=60, split=False)
    if len(Summary)>1:
        subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
def ScrapeLiveMint11(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<2):
        URL = "https://www.livemint.com/mostpopular"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='listView')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="listing clearfix impression-candidate"):
            try:
                print(1)
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['alt']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataLiveMint11(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveMint11(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file11(subdict)
def GatherDataJagran11(i,d,PostHeading,subdict):
    try:
    # andre wali post ka url
        PostUrl = "https://english.jagran.com"+i.find('a')['href']
        print(PostUrl)
        # post image ka url
        PostImageAddress=i.find('img')['data-src']
        if not PostImageAddress.startswith('http'):
            PostImageAddress = "https:" + i.find('img')['data-src']
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='articleBody')
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        Summary=Shorten11(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        pass
def ScrapeJagran11(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://english.jagran.com/latest-news-page"+str(c)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            value=(float(time.time())-clock)
            print(count,value)
            count+=1
            try:
                PostHeading=i.find("img",class_='lazy')["alt"]
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataJagran11(i,d,PostHeading,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran11(i,d,PostHeading,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
        #picle me dictionary store kr rahe  hai
    write_to_file11(subdict)
def GatherDataHindustanTimes11(i,d,subdict):
    PostUrl =i.find('a')['href']
    print(PostUrl)
    PostHeading=i.find('img')['title']
    agent = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(PostUrl,headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article=soup.find('div',class_='storyDetail')
    PostComplete=""
    for j in article.findAll('p'):
        PostComplete+=j.text
    PostImageAddress=soup.find('figure').find('img')['src']
    Summary=Shorten11(PostComplete,PostHeading)
    print(PostHeading)
    print(PostImageAddress)
    if len(Summary)>1:
        subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
def ScrapeHindustanTimes11(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    # a="latest-news-morenews more-latest-news more-separate newslist-sec"
    while(c<4):
        if c>1:
            a="latest-news-bx more-latest-news more-separate"
        URL = "https://www.hindustantimes.com/latest-news/?pageno="+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_="latest-news-bx more-latest-news more-separate")
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes11(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes11(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file11(subdict)
def GatherDataZeeNews11(i,d,subdict):
    PostUrl ="https://zeenews.india.com"+i.find('a')['href']
    PostHeading=i.find('img')['title']
    agent = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(PostUrl,headers=agent).text
    soup = BeautifulSoup(r, 'lxml')
    article=soup.find('div',class_='article-right-col main')
    PostComplete=""
    for j in article.findAll('p'):
        PostComplete+=j.text
    PostImageAddress=soup.find('div',class_='article-image-block margin-bt30px').find('img')['src']
    translator = Translator()
    PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
    Summary=Shorten11(PostComplete,PostHeading)
    if len(Summary)>1:
        subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
def ScrapeZeeNews11(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    while(c<2):
        URL = "https://zeenews.india.com/latest-news"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',class_='maincontent')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="section-article margin-bt30px clearfix"):
            try:
                if c>=60:
                    break
                c+=1
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataZeeNews11(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataZeeNews11(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file11(subdict)
def ScrapSuper11(i,d,isNewsPickle):
    if i==0:
        ScrapeJagran11(d,isNewsPickle)
    if i==1:
        ScrapeLiveMint11(d,isNewsPickle)
    if i == 2:
        ScrapeHindustanTimes11(d, isNewsPickle)
    if i == 3:
        ScrapeZeeNews11(d, isNewsPickle)
def scrape_trending_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(4):
            p = threading.Thread(target=ScrapSuper11, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData11))
        post_data = {"news_type": "trending_news", "news": []}
        for data in ScrapedData11.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData11.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#               END TRENDING NEWS SCRAPER               #
#                                                       #
#########################################################



#########################################################
#                                                       #
#              START POLITICS NEWS SCRAPER              #
#                                                       #
#########################################################



ScrapedData12 = dict()
def write_to_file12(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData12.update(subdict)
    global_lock.release()
def Shorten12(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataLiveMint12(i,d,subdict):
    try:
        PostUrl ="https://www.livemint.com"+i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="contentSec")
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('section',class_='cardHolder open').find('img')['alt']
        Summary=Shorten12(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("is mai error aaya")
def ScrapeLiveMint12(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<2):
        URL = "https://www.livemint.com/politics/news"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='listView')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="listing clearfix impression-candidate"):
            try:
                print(1)
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['alt']
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataLiveMint12(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveMint12(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file12(subdict)
def GatherDataNews1812(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='article-box')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=article.find('img')['src']
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten12(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("iss mai error aaya -->")
def ScrapeNews1812(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0
    while(c<3):
        URL = "https://www.news18.com/politics/page-"+str(c)+"/"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='blog-list')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="blog-list-blog"):
            try:
                if c>=60:
                    break
                c+=1
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['alt']
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataNews1812(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataNews1812(i,d,subdict)
            except Exception as e:
                print(e)
                continue
        c+=1
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file12(subdict)
def GatherDataEconomicTimes12(i,d,PostHeading,subdict):
    try:
    # andre wali post ka url
        PostUrl = "https://economictimes.indiatimes.com"+i.find('a')['href']
        print(PostUrl)
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('article',class_='artData clr')
        PostImageAddress=PostArticle.find('figure',class_="artImg").find('img')['src']
        print(PostImageAddress)
        PostComplete=PostArticle.text
        Summary=Shorten12(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except Exception as e:
        print(e)
def ScrapeEconomicTimes12(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<2):
        URL = "https://economictimes.indiatimes.com/news/politics-nation"
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('section',id='bottomPL')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        j=0
        for i in article.findAll('div',class_="botplData flt"):
            print(j)
            j+=1
            value=(float(time.time())-clock)
            print(count,value)
            count+=1
            try:
                PostHeading=i.find('span',class_="imgContainer").find("img")["alt"]
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataEconomicTimes12(i,d,PostHeading,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataEconomicTimes12(i,d,PostHeading,subdict)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file12(subdict)
def ScrapSuper12(i,d,isNewsPickle):
    if i==0:
        ScrapeLiveMint12(d,isNewsPickle)
    if i==1:
        ScrapeNews1812(d,isNewsPickle)
    if i == 2:
        ScrapeEconomicTimes12(d, isNewsPickle)
def scrape_politics_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper12, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData12))
        post_data = {"news_type": "politics_news", "news": []}
        for data in ScrapedData12.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData12.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#               END POLITICS NEWS SCRAPER               #
#                                                       #
#########################################################



#########################################################
#                                                       #
#              START SPORTS NEWS SCRAPER                # 
#                                                       #
#########################################################



ScrapedData13 = dict()
def write_to_file13(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData13.update(subdict)
    global_lock.release()
def Shorten13(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataIndainExpress13(i,d,subdict,PostHeading):
    try:
        PostUrl =i.find('h2',class_="title").find('a')['href']
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="full-details")
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('span',class_='custom-caption').find('img')['src']
        Summary=Shorten13(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeIndainExpress13(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://indianexpress.com/section/sports/page/"+str(c)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='nation')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="articles"):
            try:
                print(1)
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h2',class_="title").text.replace("\n","")
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataIndainExpress13(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataIndainExpress13(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file13(subdict)
def GatherDataHindustanTimes13(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='storyDetail')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('figure').find('img')['src']
        Summary=Shorten13(PostComplete,PostHeading)
        print(PostHeading)
        print(PostImageAddress)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya")
def ScrapeHindustanTimes13(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    a="latest-news-morenews more-latest-news more-separate newslist-sec"
    while(c<4):
        if c>1:
            a="latest-news-bx more-latest-news more-separate"
        URL = "https://www.hindustantimes.com/sports-news/page/?pageno="+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_=a)
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes13(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes13(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file13(subdict)
def ScrapSuper13(i,d,isNewsPickle):
    if i==0:
        ScrapeIndainExpress13(d,isNewsPickle)
    if i==1:
        ScrapeHindustanTimes13(d,isNewsPickle)
def scrape_sports_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(2):
            p = threading.Thread(target=ScrapSuper13, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData13))
        post_data = {"news_type": "sports_news", "news": []}
        for data in ScrapedData13.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData13.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#                END SPORTS NEWS SCRAPER                # 
#                                                       #
#########################################################



#########################################################
#                                                       #
#           START BOLLYWOOD NEWS SCRAPER                # 
#                                                       #
#########################################################



ScrapedData14 = dict()
def write_to_file14(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData14.update(subdict)
    global_lock.release()
def Shorten14(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataHindustanTimes14(i,d,subdict):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        PostHeading=i.find('img')['title']
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='storyDetail')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('figure').find('img')['src']
        Summary=Shorten14(PostComplete,PostHeading)
        print(PostHeading)
        print(PostImageAddress)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya")
def ScrapeHindustanTimes14(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    a="latest-news-morenews more-latest-news more-separate newslist-sec"
    while(c<4):
        if c>1:
            a="latest-news-bx more-latest-news more-separate"
        URL = "https://www.hindustantimes.com/bollywood/page/?pageno="+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_=a)
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataHindustanTimes14(i,d,subdict)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataHindustanTimes14(i,d,subdict)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")
    write_to_file14(subdict)
def GatherDataJagran14(i,d,subdict,PostHeading):
    try:
        # andre wali post ka url
        PostUrl = "https://www.jagran.com"+i.find('a')['href']
        print(PostUrl)
        # post image ka url

        # post ki heading
        
        # post ka content uske url pr jakr extract kr re
        PortReq = requests.get(PostUrl).text
        Postsoup = BeautifulSoup(PortReq, 'lxml')
        PostArticle=Postsoup.find('div',class_='articleBody')
        PostImageAddress=Postsoup.find('img')['src']
        print(PostImageAddress)
        PostComplete=""
        for j in PostArticle.findAll('p'):
            PostComplete+=j.text
        translator = Translator()
        PostComplete = translator.translate(PostComplete,src='hi',dest='en').text
        Summary=Shorten14(PostComplete,PostHeading)
        Summary = translator.translate(Summary,dest='en').text
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeJagran14(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<4):
        URL = "https://www.jagran.com/entertainment/bollywood-news-hindi-page"+str(c)+".html"
        print(URL)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('ul',class_='topicList')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('li'):
            try:
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('div',class_='h3').text
                t=Translator()
                PostHeading=t.translate(PostHeading,src='hi',dest='en').text
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataJagran14(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataJagran14(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file14(subdict)
def GatherDataLiveMint14(i,d,subdict,PostHeading):
    try:
        PostUrl =i.find('a')['href']
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="full-details")
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('img')['alt']
        Summary=Shorten14(PostComplete,PostHeading)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]  
    except:
        print("ismai error aaya -->",PostHeading)   
def ScrapeLiveMint14(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0   
    while(c<2):
        URL = "https://indianexpress.com/section/entertainment/bollywood/page/"+str(c)+"/"
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='nation')
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="articles"):
            try:
                print(1)
                if c>=60:
                    break
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('div',class_="title").text
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataLiveMint14(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataLiveMint14(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
                continue
        if flag==1:
                break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
        #reversing the dict for restoring the order
    # subdict=OrderedDict(reversed(list(subdict.items())))
        #picle me dictionary store kr rahe  hai
    write_to_file14(subdict)
def ScrapSuper14(i,d,isNewsPickle):
    if i==0:
        ScrapeHindustanTimes14(d,isNewsPickle)
    if i==1:
        ScrapeJagran14(d,isNewsPickle)
    if i == 2:
        ScrapeLiveMint14(d, isNewsPickle)
def scrape_bollywood_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper14, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData14))
        post_data = {"news_type": "bollywood_news", "news": []}
        for data in ScrapedData14.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData14.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#             END BOLLYWOOD NEWS SCRAPER                # 
#                                                       #
#########################################################



#########################################################
#                                                       #
#             START FAKE NEWS SCRAPER                   # 
#                                                       #
#########################################################



ScrapedData23 = dict()
def write_to_file23(subdict):
    while global_lock.locked():
        continue
    global_lock.acquire()
    ScrapedData23.update(subdict)
    global_lock.release()
def Shorten23(PostComplete,PostHeading):
    a=summarize(PostComplete,ratio=3, split=True)
    Summary=""
    for i in a:
        if(len(Summary.split())+len(i.split())<=70-len(PostHeading.split())):
            Summary+=i
        elif(len(Summary.split())+len(PostHeading.split())<=50):
            continue
        else:
            break
    return Summary
def GatherDataBoomLive23(i,d,subdict,PostHeading):
    try:
        PostUrl ="https://www.boomlive.in"+i.find('a')['href']
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='story')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_="single-featured-thumb-container").find('img')['src']
        print(PostImageAddress)
        Summary=Shorten23(PostComplete,PostHeading)
        print(PostHeading)
        print(PostImageAddress)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeBoomLive23(d,isNewsPickle):
    c=1
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<4):
        URL = "https://www.boomlive.in/fake-news/"+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="category-articles-list listing-article-list")
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="card-wrapper horizontal-card"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('img')['title']
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataBoomLive23(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataBoomLive23(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file23(subdict)
def GatherDataIndiaToday23(i,d,subdict,PostHeading):
    try:
        PostUrl ="https://www.indiatoday.in"+i.find('a')['href']
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='description')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        PostImageAddress=soup.find('div',class_="stryimg").find('img')['data-src']
        print(PostImageAddress)
        Summary=Shorten23(PostComplete,PostHeading)
        PostHeading=PostHeading.split("Fact Check:")[1]
        print(PostHeading)
        print(PostImageAddress)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeIndiaToday23(d,isNewsPickle):
    c=0
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<4):
        URL = "https://www.indiatoday.in/fact-check?page="+str(c)
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="view-content")
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="catagory-listing"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h2').text
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataIndiaToday23(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataIndiaToday23(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file23(subdict)
def GatherDataFactly23(i,d,subdict,PostHeading):
    try:
        PostUrl =i.find('a',class_="image-link")['href']
        print(PostUrl)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(PostUrl,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='post-content-right')
        PostComplete=""
        for j in article.findAll('p'):
            PostComplete+=j.text
        t=Translator()
        PostComplete=t.translate(PostComplete,dest="en").text
        PostImageAddress=soup.find('div',class_="wp-block-image").find('img')['src']
        Summary=Shorten23(PostComplete,PostHeading)
        Summary=t.translate(Summary,dest="en").text
        print(PostImageAddress)
        if len(Summary)>1:
            subdict[PostHeading]=[PostUrl,PostImageAddress,PostHeading,Summary]
    except:
        print("ismai error aaya -->",PostHeading)
def ScrapeFactly23(d,isNewsPickle):
    c=0
    # dictionary store kregi  d[PostHeading]=[PostUrl,PostImageAddress,PostHeading,PostComplete]
    subdict=OrderedDict()
    #reprocessing se bachane k liye
    flag=0
    count=0 
    while(c<1):
        URL = "https://factly.in/category/fake-news/"
        print(URL)
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(URL,headers=agent).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_="row b-row listing meta-below grid-2")
        count=0
        clock=float(time.time())
        print("start",(float(time.time())-clock))
        for i in article.findAll('div',class_="column half b-col"):
            try:
                if(not i.find('img')):
                    continue
                value=(float(time.time())-clock)
                print(count,value)
                count+=1
                PostHeading=i.find('h2').text
                t=Translator()
                PostHeading=t.translate(PostHeading,dest="en").text
                print(PostHeading)
                if isNewsPickle==1:
                    if PostHeading not in d:
                        GatherDataFactly23(i,d,subdict,PostHeading)
                    else:
                        flag=1
                        print("----->bas itna hi update hua hai.... baki apne paas already hai")
                        break
                else:
                    GatherDataFactly23(i,d,subdict,PostHeading)
            except Exception as e:
                print(e)
        if flag==1:
            break
        c+=1
    print(len(subdict),"artiles updated in from indiatoday")  
    #reversing the dict for restoring the order
    #subdict=OrderedDict(reversed(list(subdict.items())))
    #picle me dictionary store kr rahe  hai
    write_to_file23(subdict)    
def ScrapSuper23(i,d,isNewsPickle):
    if i==1:
        ScrapeBoomLive23(d,isNewsPickle)
    if i==2:
        ScrapeFactly23(d,isNewsPickle)
    if i==0:
        ScrapeIndiaToday23(d,isNewsPickle)
def scrape_fake_news(languages, pickle_file):
    translator = Translator()
    translator2 = Translator()
    while True:
        print("Scraping")
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                d = pickle.load(f)
        else:
            d = []
        threads = []
        for i in range(3):
            p = threading.Thread(target=ScrapSuper23, args=(i, d, 1, ))
            threads.append(p)
            p.start()
        [thread.join() for thread in threads]
        print("Scraping done")
        print(len(ScrapedData23))
        post_data = {"news_type": "fake_news", "news": []}
        for data in ScrapedData23.values():
            post_data["news"].append({"english": [html.unescape(data[2].replace("\n", " ")), html.unescape(data[3].replace("\n", " ")), data[1], data[0]], "others": [[i, (translator.translate(data[2].replace('\n', ' '), src='en', dest=i)).text, (translator2.translate(data[3].replace('\n', ' '), src='en', dest=i)).text] for i in languages]})
            d.append(data[2])
        with open(pickle_file, "wb") as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        del d
        print(post_data)
        random.shuffle(post_data["news"])
        ret = requests.post(POST_URL, json=post_data)
        print(ret)
        ScrapedData23.clear()
        time.sleep(1800)



#########################################################
#                                                       #
#             END FAKE NEWS SCRAPER                     # 
#                                                       #
#########################################################



def MegaScrapeSuper(i):
    if i == 0:
        scrape_world_news(ALLOWED_LANGUAGES, WORLD_NEWS_PICKLE_FILE)
    elif i == 1:
        scrape_national_news(ALLOWED_LANGUAGES, NATIONAL_NEWS_PICKLE_FILE)
    elif i == 2:
        scrape_tech_news(ALLOWED_LANGUAGES, TECH_NEWS_PICKLE_FILE)
    elif i == 3:
        scrape_state_karnataka_news(ALLOWED_LANGUAGES, KARNATAKA_NEWS_PICKLE_FILE)
    elif i == 4:
        scrape_state_uttarpradesh_news(ALLOWED_LANGUAGES, UTTARPRADESH_NEWS_PICKLE_FILE)
    elif i == 5:
        scrape_state_uttarpradesh_district_news(ALLOWED_LANGUAGES, UTTARPRADESH_DISTRICT_NEWS_PICKLE_FILE, UTTARPRADESH_DISTRICTS)
    elif i == 6:
        scrape_state_karnataka_district_news(ALLOWED_LANGUAGES, KARNATAKA_DISTRICT_NEWS_PICKLE_FILE, KARNATAKA_DISTRICTS)
    elif i == 7:
        scrape_state_delhi_news(ALLOWED_LANGUAGES, DELHI_NEWS_PICKLE_FILE)
    elif i == 8:
        scrape_state_maharashtra_news(ALLOWED_LANGUAGES, MAHARASHTRA_NEWS_PICKLE_FILE)
    elif i == 9:
        scrape_state_maharashtra_district_news(ALLOWED_LANGUAGES, MAHARASHTRA_DISTRICT_NEWS_PICKLE_FILE, MAHARASHTRA_DISTRICTS)
    elif i == 10:
        scrape_trending_news(ALLOWED_LANGUAGES, TRENDING_NEWS_PICKLE_FILE)
    elif i == 11:
        scrape_politics_news(ALLOWED_LANGUAGES, POLITICS_NEWS_PICKLE_FILE)
    elif i==12:
        scrape_sports_news(ALLOWED_LANGUAGES, SPORTS_NEWS_PICKLE_FILE)
    elif i==13:
        scrape_bollywood_news(ALLOWED_LANGUAGES, BOLLYWOOD_NEWS_PICKLE_FILE)
    elif i==14:
        scrape_state_westbengal_news(ALLOWED_LANGUAGES,WESTBENGAL_NEWS_PICKLE_FILE) 
    elif i == 15:
        scrape_state_westbengal_district_news(ALLOWED_LANGUAGES, WESTBENGAL_DISTRICT_NEWS_PICKLE_FILE, WESTBENGAL_DISTRICTS)
    elif i == 16:
        scrape_state_gujarat_news(ALLOWED_LANGUAGES, GUJARAT_NEWS_PICKLE_FILE)
    elif i == 17:
        scrape_state_gujarat_district_news(ALLOWED_LANGUAGES, GUJARAT_DISTRICT_NEWS_PICKLE_FILE, GUJARAT_DISTRICTS)
    elif i == 18:
        scrape_state_andhrapradesh_news(ALLOWED_LANGUAGES, ANDHRAPRADESH_NEWS_PICKLE_FILE)
    elif i == 19:
        scrape_state_andhrapradesh_district_news(ALLOWED_LANGUAGES, ANDHRAPRADESH_DISTRICT_NEWS_PICKLE_FILE, ANDHRAPRADESH_DISTRICTS)
    elif i == 20:
        scrape_state_rajasthan_news(ALLOWED_LANGUAGES, RAJASTHAN_NEWS_PICKLE_FILE)
    elif i == 21:
        scrape_state_rajasthan_district_news(ALLOWED_LANGUAGES, RAJASTHAN_DISTRICT_NEWS_PICKLE_FILE, RAJASTHAN_DISTRICTS)
    elif i==22:
        scrape_fake_news(ALLOWED_LANGUAGES, FAKE_NEWS_PICKLE_FILE)
if __name__ == '__main__':
    try:
        masterthreads = []
        for i in range(N):
            p = threading.Thread(target=MegaScrapeSuper, args=(i, ))
            masterthreads.append(p)
            p.start()
        [thread.join() for thread in masterthreads]
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)