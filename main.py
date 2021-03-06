#! python3
import praw
import pandas as pd
import csv
import yahoo_fin as yf
import requests
import requests_html
import io
import ftplib
import nltk
import yahoo_fin.stock_info as si

nltk.download('stopwords')
stopWords = nltk.corpus.stopwords.words('english')

reddit = praw.Reddit(client_id="2SnfVtrgAb-prQ", client_secret="SEhhHIKln8MXWY4-TeyJbIk7MXWyLQ", user_agent="reddit_stocks")

sub = reddit.subreddit("wallstreetbets")

#Create dictionary from csv with key = ticker and val = word counts
csvName = "nasdaq.csv"
with open(csvName, mode='r') as fin:
    reader = csv.reader(fin)
    tickerCounts = {rows[0]:0 for rows in reader}

#tickerCounts = {tick:0 for tick in si.tickers_nasdaq()}

# display the subreddit name 
print(sub.display_name) 
#Retrieve comment from specified subreddit and append to list
def getComments(submissionList):
    commentList = []
    for submission in submissionList:
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            
            if(isinstance(comment.body, str)):
                commentList.append(comment.body)
                #print(comment.body.encode("utf-8"))
    return commentList

def getSubmissions(sub, numSubmissions):
    submissionList = []
    for submission in sub.hot(limit=numSubmissions):
        submissionList.append(submission)
    return submissionList

def screenWords(commentList, tickerDict):
    for comment in commentList:
        cList = comment.split()
        for word in cList:
            #print(word)
            if word.upper() in tickerCounts.keys():
                tickerCounts[word.upper()] += 1
            elif word[0] == "$" and word.upper()[1:] in tickerCounts.keys():
                tickerCounts[word.upper()[1:]] += 1
               
def printSorted(tickerDict):
    sortedTickers = sorted(tickerDict, key=tickerDict.get, reverse=False)
    #print(sortedTickers)
    finalTickers = [x for x in sortedTickers if x.lower() not in stopWords]
    for ticker in finalTickers:
       if tickerDict[ticker] > 10:
           print(ticker, tickerDict[ticker])

def getStockPrice(ticker):
    gme_week = si.get_data(ticker, start_date="12/04/2009", end_date="1/22/2021", index_as_date = True, interval="1wk")
    print(gme_week)

    




subList = getSubmissions(sub,100)
commentList = getComments(subList)
screenWords(commentList, tickerCounts)
printSorted(tickerCounts)
#get_day_gainers()
#getStockPrice("gme")


