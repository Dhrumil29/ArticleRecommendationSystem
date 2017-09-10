import string
import urllib
import pymongo
import re
import math
from string import digits
from string import punctuation
from reverse_index import ReverseIndex
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nlp
import json
#
#Paremeters:
    # Soup extracted from the webpage
    # Links Array of links
#
def get_links(soup,links,count):
    #print("soup",links,count)
    wiki = links[count-1]
    if len(soup)>0:
        for link in soup.find_all(href=re.compile("/2016/")):
            if link not in links:
                if "www." in link.get('href'):
                        if "engadget" in link.get('href') :
                            links.append(link.get('href'))
                        elif "https" not in link.get('href'):
                            links.append("https://www.engadget.com"+link.get('href'))
        for link in soup.find_all(href=re.compile("/2017/")):
            if link not in links:
                if "www." in link.get('href'):
                    if "engadget" in link.get('href'):
                        links.append(link.get('href'))
                    elif "https" not in link.get('href'):
                        links.append("https://www.engadget.com" + link.get('href'))
        link_array_length = len(links)
        #print(links)

    connect_and_get_keywords(wiki,links,count)


def get_keywords_frequencies(wiki,links,count):
    #print(wiki,links,count)
    try:
        page = urllib.request.urlopen(wiki).read()
        soup = BeautifulSoup(page, "lxml")
        article_text = []
        keywords = []
        for tags in soup.find_all("div", class_="article-text"):
            article_text.append(tags.text)
        for tags in soup.find_all("span", class_="th-meta"):
            keywords.append(tags.text)
        # article_body=soup.body.text
        if len(keywords) > 0:
            start_idx = [i for i, item in enumerate(keywords) if item.startswith('\n')]
            if len(start_idx) > 0:
                print(start_idx)
                start_index = start_idx[0]
                print(keywords)
                keywords = keywords[start_index:]
                print(keywords)
                keyword_string = keywords[0]
                # keywords=keyword_string.split(",")
                # print (keywords)
                # print article_text
                article_body = ''.join(article_text)

                # ReverseIndex((nlp.do_stemming(article_body))
                #
                #
                # print len(text)
                # for wikipedia
                # for tags in soup.find_all("body", class_="mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject page-Hidden_Markov_model rootpage-Hidden_Markov_model skin-vector action-view"):
                #    article_body = tags.text

                cachedStopWords = stopwords.words("english")

                article_body = ' '.join([word for word in article_body.split() if word not in cachedStopWords])
                print(article_body)
                article_body = str(article_body)
                article_body = article_body.translate(punctuation)
                translator = str.maketrans({key: None for key in string.punctuation})
                article_body = article_body.translate(translator)
                keyword_string = keyword_string.translate(translator)
                # article_body=article_body.translate(None,digits)

                # article_body=" ".join((map(str,article_body)))
                #print(article_body)
                tokens = nlp.do_stemming(article_body.split())
                keyword_tokens = nlp.do_stemming(keyword_string.split())
                #print(tokens)
                #print(keyword_tokens)
                index = ReverseIndex(" ".join(map(str, tokens)))
                index.generate_index()
                #print(index.index)
                #print(index.text)
                for i, val in enumerate(keyword_tokens):
                    keyword=val
                    try:
                        connection = pymongo.MongoClient()
                    except:
                        print("MongoDB Connection not established")
                    db = connection.testing

                    keywords = db.keywords
                    #url = db[wiki].update()

                    weight_of_keyword = 1000 + math.pow(3,i)
                    #print(keywords[val].update())
                    print(keywords[val].insert_one({"url":wiki,"weight":weight_of_keyword}))
                    #keywords database make and links inserting
                    print(i, val, ":", index.find_index(val))
                    connection.close()
                # print(index.index("23andme"))
                # for i in keyword_tokens:
                #     print(index.get(keyword_tokens[i]))

                # print len(text)
                # body_text=text.split(' ')
                # print body_text
                # print text
                # is_it=text.find("virtual reality")
                # print is_it
                # #scikit learn  tf-idf pickle
    except:
        print("Link Not good")
        count= count+1
        soup=""

    get_links(soup,links,count)


            # link="https://www.engadget.com"+val
            #
            # print(link)
            # connect_and_get_keywords(link)
def connect_and_get_keywords(wiki,links,count):
    #print(wiki,links,count)
    index=count
    # print("it came here!")
    # print(wiki)
    link_array_length = len(links)
    for i,val in enumerate(links):
        if i >= index & i < link_array_length:
            try:
                connection = pymongo.MongoClient()
            except:
                print("MongoDB Connection not established")
            wiki = val
            db = connection.testing
            url_list = db.url

            if not (url_list.find_one({"url": wiki})):
                # print(wiki, "is already in database")
                #else:
                print("inserting", wiki)
                url_list.insert_one({"url": wiki})
                connection.close()
                get_keywords_frequencies(wiki, links, index)

    # for i, val in enumerate(links[0:]):
    #     index = index + 1
    #     if index >= count & index < link_array_length:
    #         if val.find("www.") == -1:
    #             print("no www. is found in", val)
    #         else:
    #             try:
    #                 connection = pymongo.MongoClient()
    #             except :
    #                 print("MongoDB Connection not established")
    #             db = connection.testing
    #             url_list = db.url
    #             if(url_list.find_one({"url":wiki})):
    #                 print(wiki,"is already in database")
    #             else:
    #                 print("inserting",wiki)
    #                 print(url_list.insert_one({"url":wiki}))
    #                 get_keywords_frequencies(wiki,links,index)
    #


# #wiki ="http://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/"
# #wiki="http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/"
# #wiki="http://www.gizmodo.in/science/Your-Self-Driving-Car-Will-Be-Programmed-to-Kill-You-Deal-With-It/articleshow/52891419.cms"
#wiki="http://www.gizmodo.in/gadgets/Two-Women-Go-Blind-After-Checking-Phone-in-Bed/articleshow/52887879.cms"
#wiki="http://www.gizmodo.in/gadgets/A-Motion-Detecting-Camp-Lantern-Promises-to-Keep-Blair-Witches-at-Bay/articleshow/52871646.cms"
# wiki="http://www.gizmodo.in/indiamodo/6-Ways-In-Which-Commuting-Is-Rapidly-Changing-In-India/articleshow/52934000.cms"
#wiki="http://www.gizmodo.in/science/8-Ways-Virtual-Reality-Is-For-More-Than-Just-Video-Games/articleshow/52930810.cms"
#wiki1=input("Enter the link\n")
#wiki="https://www.engadget.com/2016/08/02/23andme-data-helps-find-depression-genetics/"
#wiki="https://en.wikipedia.org/wiki/Hidden_Markov_model"
#wiki="http://mashable.com/2016/08/02/tesla-pokemon-go-hack/#xDMlejA5Wqqz"
#wiki="http://www.gizmodo.in/science/Scientists-Find-New-Clues-In-Their-Quest-to-Understand-Why-Cocaine-Is-So-Addictive/articleshow/53496678.cms"
#wiki="http://www.gizmodo.in/indiamodo/Beware-Xiaomi-The-Lenovo-Vibe-K5-Note-Is-All-Set-To-Dethrone-The-Redmi-Note-3/articleshow/53489072.cms"
#
#wiki="http://www.gizmodo.in/indiamodo/Star-Trek-Beyond-Goes-Where-No-Trekkie-Has-Gone-Before/articleshow/53452067.cms"
#wiki="https://gigaom.com/2016/07/29/announcing-three-new-gigaom-change-2016-speakers/"
#wiki="http://www.lifehacker.co.in/jugaad/iPhone-7-Rumors-It-Might-Go-On-Sale-On-September-16/articleshow/53432904.cms"
#wiki="https://www.engadget.com/2016/08/22/fbi-finds-more-hillary-clinton-documents/"
# wiki="https://www.engadget.com/2016/08/24/amazon-kindle-reading-fund/"
# wiki="https://www.engadget.com/2016/08/24/startup-uses-algorithms-to-fund-civil-lawsuits/"
wiki="https://www.engadget.com/2016/08/24/startup-uses-algorithms-to-fund-civil-lawsuits/"
#wiki="https://www.engadget.com/2016/08/24/french-official-threatens-lawsuits-over-internet-photos/"
#wiki="https://www.engadget.com/2016/08/25/garmin-fenix-chronos-smartwatch/"
#print soup.prettify()
#print soup
# wiki="https://www.engadget.com/2016/11/10/surface-book-review-2016/"
#wiki="https://www.engadget.com/2016/09/07/iphone-7-and-7-plus-hands-on-preview/"
#wiki="https://www.engadget.com/2016/11/09/google-machine-learning-can-save-sea-cows/"
#wiki="https://www.engadget.com/2016/11/09/planet-earth-might-be-the-biggest-loser-under-president-trump/"
#wiki="https://www.engadget.com/2016/11/10/google-daydream-view-vr-review/"
#wiki="https://www.engadget.com/2016/11/10/windows-10-virtual-trackpad/"
# wiki="https://www.engadget.com/2016/11/10/oneplus-3-nougat/"
# wiki="https://www.engadget.com/2016/11/09/google-project-soli-used-to-identify-objects/"
# wiki="https://www.engadget.com/2016/10/28/google-ai-created-its-own-form-of-encryption/"
#
# wiki="https://www.engadget.com/2016/09/23/googles-ai-is-getting-really-good-at-captioning-photos/"
# wiki="https://www.engadget.com/2016/11/13/supermoon-is-largest-in-68-years/"
# wiki="https://www.engadget.com/2016/11/12/luxembourg-space-mining-law/"
wiki="https://www.engadget.com/2016/11/12/imax-raising-50-million-for-vr/"
wiki="https://www.engadget.com/2016/11/14/samsung-buys-harmon-auto-audio/"
wiki="https://www.engadget.com/2016/11/14/climate-change-temperature-hikes-could-be-worse-than-thought/"
wiki="https://www.engadget.com/2016/11/14/the-morning-after-monday-november-14-2016/"
wiki="https://www.engadget.com/2016/11/14/mit-wireless-vr/"
wiki="https://www.engadget.com/amp/2016/01/07/philips-fidelio-e6-speakers-hands-on/"
wiki="https://www.engadget.com/2016/11/14/microsoft-visual-studio-for-mac/"
wiki="https://www.engadget.com/2016/11/14/moto-z-play-review/"
wiki="https://www.engadget.com/2016/11/14/chinese-media-trumps-trade-war-will-hurt-apple-and-boeing/"
wiki="https://www.engadget.com/2016/11/14/the-martian-vr-experience-for-home/"
wiki="https://www.engadget.com/2016/11/14/google-search-for-final-election-numbers-offers-up-fake-news/"
wiki="https://www.engadget.com/2016/11/14/mars-is-much-drier-than-expected/"
wiki="https://www.engadget.com/2016/11/14/hydroelectric-dams-cause-more-emissions-than-we-thought/"
wiki="https://www.engadget.com/2016/11/14/jaguar-introduces-its-first-electric-concept-car/"
wiki="https://www.engadget.com/2016/11/15/whatsapp-finally-launches-video-calling/"
wiki="https://www.engadget.com/2016/11/15/google-photos-photoscan-app-editing-tools/"
wiki="https://www.engadget.com/2016/11/17/facebook-buys-faciometrics/"
wiki="https://www.engadget.com/2016/11/17/chrysler-hybrid-minivan/"
wiki="https://www.engadget.com/2016/11/19/lg-v20-review/"
wiki="https://www.engadget.com/2016/11/28/samsung-considers-new-structure/"
wiki="https://www.engadget.com/2017/03/10/samsung-completes-its-biggest-acquisition-ever/"
wiki="https://www.engadget.com/2017/03/10/google-insists-hangouts-for-consumers-isnt-going-away/"
wiki="https://www.engadget.com/2017/03/10/new-us-solar-installations-nearly-doubled-in-2016/"
wiki="https://www.engadget.com/2017/03/08/icymi-roving-robots-measure-health-vitals/"
wiki="https://www.engadget.com/2017/03/04/nasa-prevents-maven-phobos-collision/"
wiki="https://www.engadget.com/2017/03/08/nintendo-switch-one-week/"
wiki="https://www.engadget.com/2017/08/29/youtube-redesign-desktop-ios-android/"
wiki="https://www.engadget.com/2017/08/29/google-pulls-300-android-apps-wirex-ddos/"
# link_dictionary=dict()
# for variable in soup.find_all("meta",  name="keywords"):
#         variable=soup.find("meta",  name="keywords")
#         print(variable["content"])
#
#
# keyword=dict()
#
# for tags in soup.find_all("meta"):
#     metaname = tags.get('name', '').lower()
#     if metaname=="keywords":
#         keywords=x.split(',')
#         print keywords

links=[]
links.append(wiki)
text="snakln"
print("Starting the run:")
connect_and_get_keywords(wiki,links,1)
# # # # #
Term= input("Enter the term for which you want to see the best article of 2016 according to my analysis?")
stemmed_term=LancasterStemmer().stem(Term)
print(stemmed_term)
try:
    connection = pymongo.MongoClient()
except:
    print("MongoDB Connection not established")
db = connection.testing

keywords = db.keywords
for post in keywords[stemmed_term].find().sort("weight",-1):
    print(post)
