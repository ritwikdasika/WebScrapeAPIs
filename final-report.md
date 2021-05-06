# Web Scraping The NYTimes Most Popular Articles API

As I was exploring the New York Times APIs, a few of them intrigued me. I decided to take a look at the
most viewed articles in the last 30 days using the Most Popular API available on the developer.nytimes.com
website. As I continued to explore this API, I saw that there were a few paths I could use:

1. Most emailed articles within a specified period of time (the last 1, 7, or 30 days)
2. Most shared articles within a specified period of time (the last 1, 7, or 30 days)
3. Most viewed articles on NYTimes.com within a specified period of time (the last 1, 7, or 30 days)

We live in a digital age where information can be shared and circulated in a matter of minutes, maybe seconds. Even for a huge mass media company like The New York Times, sometimes the most effective way 
to get your news circulating comes from your consumers sharing the articles on mainstream social media
websites. 

That begs me to ask the question - over the last 30 days, how many of the most viewed articles on the NY Times website ended up being shared on Facebook? What are people reading about and sharing? I would also like to know the keywords of those articles as they can give me a good idea of the topics that are trending. 

I will implement an ETL process using Python and the viewed and shared paths available on the NY Times Most Popular API to find out. 

> *Note: I will be using FireFox to view the JSON data, simply because FireFox structures the data in an organized and neat manner that is pleasing to look at and easy to work with.

---

## Code Walkthrough

### Packages

You will need to import the following libraries:

![Import](https://i.ibb.co/XZz1Wqb/import-fin.png)

I'll provide a brief description of each library:

- requests - Requests is a library that allows users to send HTTP requests with ease. We will use the json method to retrieve the data for this project in the extract function.
- csv - This is a module available in the Python Standard Library which can read and write data in a CSV format. We will be using it in our loading function to neatly organize the data into a csv.
- prettytable - This is a Python library that allows us to display data in a visually pleasing tabular format. We will be using it in our code to print a table with the article titles, sections, date published, and the number of keywords in each article.

### Extraction

We will start by extracting the data using the following code:

> *Note: I have not shown my API key for privacy reasons. You will have to define your API key - which will be provided when you create a Developer account on developer.nytimes.com - as a string variable before you create your extract function, shown in the below image. 

![Extract](https://i.ibb.co/bKxH3YP/extract-fin.png)

Here, I will access the two API links and use two data objects to store the unprocessed data. From here, the process is pretty simple:

- I create a list called newlist. 
- Using the for loop, I will iterate through the data object vieweddata['results']
- for each dictionary within that object, I will check to see if the same dictionary exists in the shareddata['results'] object. 
- If there is a match, I will append this dictionary to the newlist.

### Transform

In our transform function, we want to get certain data about the articles, which is:

- The title
- The author
- The secion
- The keywords
- The number of keywords

Most of the code shown below is self explanatory, however I will elaborate on obtaining the number of keywords.

![Transform](https://i.ibb.co/fSSkGvx/transform-fin.png)

We declare a counter, which we will name keyword_count, to keep track of the number of keywords in each article. To be extra careful, we will convert the value of temp['keywords'] into a string. 

The keywords for one of the articles in our data looks like this:

<p>
<span style="color:green">
your-feed-science;Disease Rates;Coronavirus (2019-nCoV);Epidemics;Vaccination and Immunization;United States
</span>
</p>

There are six keywords. Notice how there is a semi-colon between each keyword. We can use the number of semi-colons to determine the number of keywords. However, there is no semi-colon at the very end. Because of this, the count will return 5 as the total number of keywords - this is wrong. Therefore, to include the final keyword, we will add 1 to the value of keyword_count.

### Using PrettyTable to output a pretty table

We'll use the prettytable library to neatly present our data:

![PrettyTable](https://i.ibb.co/c3rqfNz/prettytable-fin.png)

To make it look neater, I will not print the keywords - they will instead be in our csv. 
For now, I just want to see the title, the section, the date, and the number of keywords in each article.

However, I want to go into more detail. I want to see the most common trending keywords from the articles in tabular format to get a better glimpse of the hottest topics in the past 30 days. I will use the following code:

![keytable](https://i.ibb.co/1KXCjrb/keytable-fin.png)

We use two instances of list comprehension to perform two tasks:
- Replace duplicate dictionaries.
- Delete some less important dictionaries containing keywords like 'and'.

Then we will sort the list by highest number of keyword instances using the sorted() function and lambda.

### Loading

Now we will use the csv module to write our data to a csv file. We first need to create a file object.

We create a file object called 'outputfile'.

![Loading](https://i.ibb.co/gJ2rnQC/load-fin.png)

We then write to the file using DictWriter, which uses 'keys' to identify the order in which the values of the dictionary are written to the csv file. This is then passed to the writerows() function, which writes each row to the csv file.

With that, we have concluded the walkthrough of the code for this project.

---

## Summary of Results

The output from our first prettytable looks like this:

![table](https://i.ibb.co/BfcRSkJ/Screen-Shot-2021-05-05-at-2-34-43-PM.png)

The output from the keyword table looks like this:

![table](https://i.ibb.co/LCbcjv4/Screen-Shot-2021-05-05-at-9-54-25-PM.png)

Most of the top keywords from the articles the past 30 days are related to COVID-19. This makes sense given the current pandemic and the vaccinations being offered by Pfizer, Moderna, and the recent blood clotting issue with J&J's one shot vaccine.

To open the csv file, I will use a Microsoft Excel spreadsheet. The output looks like this:

> Keep in mind that the cells weren't expanded because it couldn't fit in a screenshot.

![excel](https://i.ibb.co/tH0NycC/Screen-Shot-2021-05-05-at-10-11-56-PM.png)

## What I Would do Next

Your code must run without errors, and it must produce data that responds to/moves your question forward (as you'll surely recall from recent video lectures.) However, there is always more work to do! If you were doing this project for realsies, what would come next? How would you improve this code in order to provide better data and a better answer?

I would make the following improvements to this code:

- Professor Allen told me about the 'Pythonic' way of writing code. I would improve my code and try to make it brief, concise, and efficient. I tend to use some naive approaches to executing tasks in Python.
- I would try to include more APIs to get geospatial/Semantic data about the most popular articles. One potential goal to explore would be listing the most common keywords of the most viewed articles by each region.

---

## The Full Python Script

```python
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

```
