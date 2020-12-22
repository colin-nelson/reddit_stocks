#! python3
import praw
import pandas as pd
import csv

reddit = praw.Reddit(client_id="2SnfVtrgAb-prQ", client_secret="SEhhHIKln8MXWY4-TeyJbIk7MXWyLQ", user_agent="reddit_stocks")

sub = reddit.subreddit("wallstreetbets")

#Create dictionary from csv with key = ticker and val = word counts
csvName = "nasdaq.csv"
with open(csvName, mode='r') as fin:
    reader = csv.reader(fin)
    tickerCounts = {rows[0]:0 for rows in reader}

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
            #print(type(word))
            if word.upper() in tickerCounts.keys():
                tickerCounts[word.upper()] += 1

def printSorted(tickerDict):
    for ticker in sorted(tickerDict, key=tickerDict.get, reverse=False):
        print(ticker, tickerDict[ticker])


subList = getSubmissions(sub,10)
commentList = getComments(subList)
screenWords(commentList, tickerCounts)
printSorted(tickerCounts)


