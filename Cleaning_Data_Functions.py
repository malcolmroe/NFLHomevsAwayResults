import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def clean2021Data (url):
    data = requests.get(url).text
    pd.set_option('display.max_columns', None)
    soup = BeautifulSoup(data, 'html5lib')
    pastOddsDF = pd.DataFrame(
        columns=['Day', 'Date', 'Time', 'Home/Away', 'Favorite', 'Score', 'Spread', 'Home/Away2', 'Underdog',
                 'Over/Under', 'Week', 'Notes'])
    range1 = 9
    weekColumn = 0
    while range1 <= 43:
        weekColumn = weekColumn + 1
        week = soup.find_all('tbody')[range1:range1 + 1]
        range1 = range1 + 2
        for row in week:
            element = row.find_all('tr')
            for x in element:
                col = x.find_all('td')
                day = col[0].text
                date = col[1].text
                time = col[2].text
                home_away = col[3].text
                favorite = col[4].text
                score = col[5].text
                spread = col[6].text
                home_away2 = col[7].text
                underdog = col[8].text
                over_under = col[9].text
                notes = col[10].text
                pastOddsDF = pastOddsDF.append(
                    {'Day': day, 'Date': date, 'Time': time, 'Home/Away': home_away, 'Favorite': favorite,
                     'Score': score, 'Spread': spread, 'Home/Away2': home_away2, 'Underdog': underdog,
                     'Over/Under': over_under, 'Week': weekColumn, 'Notes': notes}, ignore_index=True)
    favoriteTeamList = pastOddsDF['Favorite'].tolist()
    underdogTeamList = pastOddsDF['Underdog'].tolist()
    hometeamList = []
    counter = 0
    for x in pastOddsDF['Home/Away']:
        if x == '@':
            hometeamList.append(favoriteTeamList[counter])
        elif x == 'N':
            hometeamList.append('None')
        else:
            hometeamList.append(underdogTeamList[counter])
        counter = counter + 1

    pastOddsDF['Home_Team'] = hometeamList
    pastOddsDF.drop(['Home/Away', 'Home/Away2', 'Time'], axis=1, inplace=True)
    pastOddsDF.reset_index(drop=True, inplace=True)
    resultList = pastOddsDF['Score'].tolist()
    win_lossList = []
    scoreList = []
    for x in resultList:
        newList = list(x)
        win_lossList.append(newList[0])
    pastOddsDF['Favorite_Result'] = win_lossList
    pastOddsDF.reset_index(drop=True, inplace=True)
    pastOddsDF['Score'] = pastOddsDF['Score'].astype('string')
    for x in pastOddsDF['Score']:
        scoreList.append(x[2:])
    pastOddsDF['Score'] = scoreList
    scoreListReplace = [z.replace(' (OT)', '') for z in scoreList]
    favoriteScoreList = []
    underdogScoreList = []
    for x in scoreListReplace:
        favoriteScoreList.append(x.rpartition('-')[0])
        underdogScoreList.append(x.rpartition('-')[2])
    pastOddsDF['Score'] = scoreListReplace
    pastOddsDF['Favorite_Score'] = favoriteScoreList
    pastOddsDF['Underdog_Score'] = underdogScoreList
    pastOddsDF.drop('Score', axis=1, inplace=True)
    spreadList = pastOddsDF['Spread'].tolist()
    spreadListReplace = []
    spreadListResult = []
    for x in spreadList:
        spreadListReplace.append(x.rpartition('-')[2])
        spreadListResult.append(x.rpartition(' ')[0])
    counterspreadListResult = 0
    for x in spreadListResult:
        if x == 'L':
            spreadListResult[counterspreadListResult] = 0
        elif x == 'P':
            spreadListResult[counterspreadListResult] = 1
        elif x == 'W':
            spreadListResult[counterspreadListResult] = 2
        counterspreadListResult = counterspreadListResult + 1
    pastOddsDF['Spread'] = spreadListReplace
    pastOddsDF['Spread_Result'] = spreadListResult
    pastOddsDF.drop(labels=[179, 237], axis=0, inplace=True)
    pastOddsDF.reset_index(drop=True, inplace=True)
    pastOddsDF['Score_Difference'] = pastOddsDF['Favorite_Score'].astype('float') - pastOddsDF['Underdog_Score'].astype(
        'float')
    pastOddsDF['Spread_Margin'] = pastOddsDF['Score_Difference'].astype('float') - pastOddsDF['Spread'].astype('float')
    return pastOddsDF


def cleanData (url):
    data = requests.get(url).text
    pd.set_option('display.max_columns',None)
    soup = BeautifulSoup(data, 'html5lib')
    pastOddsDF = pd.DataFrame(columns=['Day','Date','Time','Home/Away','Favorite','Score','Spread','Home/Away2','Underdog','Over/Under','Week','Notes'])
    range1 = 9
    weekColumn = 0
    while range1 <= 42:
        weekColumn = weekColumn + 1
        week = soup.find_all('tbody')[range1:range1+1]
        range1 = range1 + 2
        for row in week:
            element = row.find_all('tr')
            for x in element:
                col = x.find_all('td')
                day = col[0].text
                date = col[1].text
                time = col[2].text
                home_away = col[3].text
                favorite = col[4].text
                score = col[5].text
                spread = col[6].text
                home_away2 = col[7].text
                underdog = col[8].text
                over_under = col[9].text
                notes = col[10].text
                pastOddsDF = pastOddsDF.append({'Day':day,'Date':date,'Time':time,'Home/Away':home_away,'Favorite':favorite,'Score':score,'Spread':spread,'Home/Away2':home_away2,'Underdog':underdog,'Over/Under':over_under,'Week':weekColumn,'Notes':notes}, ignore_index=True)
    favoriteTeamList = pastOddsDF['Favorite'].tolist()
    underdogTeamList = pastOddsDF['Underdog'].tolist()
    hometeamList = []
    counter = 0
    for x in pastOddsDF['Home/Away']:
        if x == '@':
            hometeamList.append(favoriteTeamList[counter])
        elif x == 'N':
            hometeamList.append('None')
        else:
            hometeamList.append(underdogTeamList[counter])
        counter = counter + 1

    pastOddsDF['Home_Team'] = hometeamList
    pastOddsDF.drop(['Home/Away','Home/Away2','Time'],axis=1,inplace=True)
    pastOddsDF.reset_index(drop=True,inplace=True)
    resultList = pastOddsDF['Score'].tolist()
    win_lossList = []
    scoreList = []
    for x in resultList:
        newList = list(x)
        win_lossList.append(newList[0])
        numberCounter = 0
    pastOddsDF['Favorite_Result'] = win_lossList
    pastOddsDF.reset_index(drop=True,inplace=True)
    pastOddsDF['Score'] = pastOddsDF['Score'].astype('string')
    for x in pastOddsDF['Score']:
        scoreList.append(x[2:])
    pastOddsDF['Score'] = scoreList
    scoreListReplace = [z.replace(' (OT)','') for z in scoreList]
    favoriteScoreList = []
    underdogScoreList = []
    for x in scoreListReplace:
        favoriteScoreList.append(x.rpartition('-')[0])
        underdogScoreList.append(x.rpartition('-')[2])
    pastOddsDF['Score'] = scoreListReplace
    pastOddsDF['Favorite_Score'] = favoriteScoreList
    pastOddsDF['Underdog_Score'] = underdogScoreList
    pastOddsDF.drop('Score',axis=1,inplace=True)
    spreadList = pastOddsDF['Spread'].tolist()
    spreadListReplace = []
    spreadListResult = []
    for x in spreadList:
        spreadListReplace.append(x.rpartition('-')[2])
        spreadListResult.append(x.rpartition(' ')[0])
    counterspreadListResult = 0
    for x in spreadListResult:
        if x == 'L':
            spreadListResult[counterspreadListResult] = 0
        elif x == 'P':
            spreadListResult[counterspreadListResult] = 1
        elif x == 'W':
            spreadListResult[counterspreadListResult] = 2
        counterspreadListResult = counterspreadListResult + 1
    pastOddsDF['Spread_Result'] = spreadListResult
    pastOddsDF['Spread'] = spreadListReplace
    pastOddsDF = pastOddsDF[pastOddsDF.Spread != 'W PK']
    pastOddsDF = pastOddsDF[pastOddsDF.Spread != 'L PK']
    pastOddsDF.reset_index(drop=True, inplace=True)
    pastOddsDF['Score_Difference'] = pastOddsDF['Favorite_Score'].astype('float') - pastOddsDF['Underdog_Score'].astype('float')
    pastOddsDF['Spread_Margin'] = pastOddsDF['Score_Difference'].astype('float') - pastOddsDF['Spread'].astype('float')
    return pastOddsDF


