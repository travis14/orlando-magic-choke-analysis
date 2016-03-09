from bs4 import BeautifulSoup 
from urllib2 import urlopen
from time import sleep
import sys
import csv
from random import randint
import collections
from collections import namedtuple

playByPlayBaseURL = "http://espn.go.com/nba/playbyplay?gameId="

GamePlayInfo = collections.namedtuple("GamePlayInfo", ["HomeTeam", "AwayTeam", "SecondsLeft", "PlayDelta", "FinalDelta"])

def getPlayFromGameID(gameID):
	gameSoup = BeautifulSoup(urlopen(playByPlayBaseURL + str(gameID)), "lxml")
	awayTeam = gameSoup.find_all("a", {"name": "&lpos=nba:game:playbyplay:clubhouse:team"})[1].find_all(text=True)[2]
	homeTeam = gameSoup.find_all("a", {"name": "&lpos=nba:game:playbyplay:clubhouse:team"})[3].find_all(text=True)[2]
	finalAwayScore = int(gameSoup.find("div", {"class": "score icon-font-after"}).find(text=True))
	finalHomeScore = int(gameSoup.find("div", {"class": "score icon-font-before"}).find(text=True))
	finalDelta = finalHomeScore - finalAwayScore

	fourthQuarterDiv = gameSoup.find("div", {"id": "gp-quarter-4"})
	plays = fourthQuarterDiv.find_all("tr")
	randomPlay = plays[randint(10, len(plays) - 10)]
	timeStamp = randomPlay.find("td", {"class": "time-stamp"}).find(text=True)
	m, s = [int(i) for i in timeStamp.split(':')]
	timeStampSecondsLeft = 60 * m + s

	timeStampScore = randomPlay.find("td", {"class": "combined-score no-change"}).find(text=True)
	timeStampAwayScore = int(timeStampScore.split('-')[0])
	timeStampHomeScore = int(timeStampScore.split('-')[1])
	timeStampDelta = timeStampHomeScore - timeStampAwayScore

	return GamePlayInfo(HomeTeam = homeTeam, AwayTeam = awayTeam, SecondsLeft = timeStampSecondsLeft, PlayDelta = timeStampDelta, FinalDelta = finalDelta)

print getPlayFromGameID(400828836)


