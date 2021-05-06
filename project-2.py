import requests
import csv
from prettytable import PrettyTable

'''
This project will implement an ETL process
and use two API links to return data
about the most viewed NY Times
articles that were also shared
to Facebook over the past 30 days.
'''

# define api key
yourkey = "8kuIiAji6NSc0EBzEKEPWisClWWlwvrA"


def nyt_extract(yourkey):
    ''' Extracts data from the nytimes API
    then finds matching dictionaries from both API links
    appends these dictionaries to newlist'''

    # view and share links with api key
    view = "https://api.nytimes.com/svc/mostpopular/v2/viewed/30.json?api-key=" + yourkey
    share = "https://api.nytimes.com/svc/mostpopular/v2/shared/30/facebook.json?api-key=" + yourkey
    head = {'user-agent': "Ritwik Dasika Final.0.0.1"}
    vieweddata = requests.get(view, headers=head).json()
    shareddata = requests.get(share, headers=head).json()
    newlist = []  # empty list
    # find matching dict between viewed and shared
    for dict in vieweddata['results']:
        if dict == dict in shareddata['results']:
            newlist.append(dict)
    return newlist


def nyt_transform(dataobj):
    '''Transforms the data from the extract function to include
    the necessary values
    Sorts the list in order of recency
    We want the title of the article, the author(s), the section, the date
    as well as any keywords and the number of keywords'''

    nyt_list = []   # empty list
    for dict in dataobj:  # by dict
        temp = {}   # create temporary dict
        temp['Title'] = dict['title']
        temp['By'] = dict['byline']
        temp['Section'] = dict['section']
        temp['Date'] = dict['published_date']
        temp['keywords'] = dict['adx_keywords']
        keyword_count = 0  # to count the number of keywords
        keywords = temp['keywords']
        keywords = str(keywords)
        for element in keywords:
            if element == ";":  # the keywords are separated by ;
                keyword_count += 1
        # add 1 because the last keyword doesn't have a semi colon after it
        temp['keycount'] = keyword_count + 1
        nyt_list.append(temp)
    # sort the list by most recent date
    nyt_list = sorted(nyt_list, key=lambda i: (i['Date']), reverse=True)
    return nyt_list


def nyt_pretty_tab(dataobj):
    '''Create a pretty table to neatly display the data we have'''
    outputTable = PrettyTable()  # create prettytable
    # establish field names
    outputTable.field_names = ["Title", "Section",
                               "Date Published", "Keywords"]
    for dict in dataobj:  # by dict
        title = dict['Title']
        section = dict['Section']
        date = dict['Date']
        keywords = dict['keycount']
        outputTable.add_row([title, section, date, keywords])  # add row
    print(outputTable)  # display table


def keywordTable(dataobj):
    '''Here, I want to return the keywords
    that occur more than once and return
    the respective count of each keyword.
    This way we can see the trending keywords
    from the most popular NY Times articles
    shared to Facebook'''

    outputTable = PrettyTable()
    outputTable.field_names = ["Keyword", "Count"]
    longstr = ""
    for dict in dataobj:
        longstr += dict['keywords']  # add keywords
    longstr = longstr.replace(';', ' ')  # replace ;
    longstr = longstr.lower()
    stringlist = longstr.split()  # create list with keywords
    newlist = []
    for item in stringlist:
        temp = {}
        temp['word'] = item
        temp['count'] = stringlist.count(item)  # num of keywords
        newlist.append(temp)
    # use list comprehension
    newlist = {frozenset(item.items()): item for
               item in newlist}.values()
    # replace duplicate dict
    newlist = [i for i in newlist if (i['count'] > 1 and i['word'] != 'and' and
               i['word'] != '(d')]  # remove dicts
    # sort the list by number of keywords
    newlist = sorted(newlist, key=lambda i: (i['count']), reverse=True)
    for dict in newlist:  # by dict
        keyword = dict['word']
        count = dict['count']
        outputTable.add_row([keyword, count])  # add row
    print(outputTable)  # display table


def nyt_load(dataobj):
    '''Load the data into an organized csv that neatly arranges data by row
    DictWriter helps create an error-free csv document
    that we can open in Excel'''

    with open("news.csv", "w", encoding='utf-8', newline="") as outputfile:
        keys = dataobj[0].keys()
        dict_writer = csv.DictWriter(outputfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataobj)

nyt_load(nyt_transform(nyt_extract(yourkey)))
nyt_pretty_tab(nyt_transform(nyt_extract(yourkey)))
keywordTable(nyt_transform(nyt_extract(yourkey)))
