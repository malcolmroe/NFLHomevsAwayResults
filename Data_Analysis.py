import pandas as pd
from Cleaning_Data_Functions import clean2021Data, cleanData
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

data2021 = clean2021Data('https://www.sportsoddshistory.com/nfl-game-season/?y=2021')
data2021['Season'] = '2021'
data2020 = cleanData('https://www.sportsoddshistory.com/nfl-game-season/?y=2020')
data2020['Season'] = '2020'
data2019 = cleanData('https://www.sportsoddshistory.com/nfl-game-season/?y=2019')
data2019['Season'] = '2019'
data2018 = cleanData('https://www.sportsoddshistory.com/nfl-game-season/?y=2018')
data2018['Season'] = '2018'
data2017 = cleanData('https://www.sportsoddshistory.com/nfl-game-season/?y=2017')
data2017['Season'] = '2017'
yearDFs = [data2021,data2020,data2019,data2018,data2017]
allData = pd.concat(yearDFs)
allData.reset_index(drop=True, inplace=True)
print(allData)
homeTeamList = allData['Home_Team'].tolist()
favoriteList = allData['Favorite'].tolist()
favoriteIsHomeTeamList = []
underdogIsHomeTeamList = []
for x in range(0,len(homeTeamList)):
    if homeTeamList[x] == favoriteList[x]:
        favoriteIsHomeTeamList.append(1)
        underdogIsHomeTeamList.append(0)
    else:
        favoriteIsHomeTeamList.append(0)
        underdogIsHomeTeamList.append(1)
favoriteScoreList = allData['Favorite_Score'].tolist()
underDogScoreList = allData['Underdog_Score'].tolist()
spreadMarginList = allData['Spread_Margin'].tolist()
homeTeamScoreList = []
awayTeamScoreList = []
homeTeamPointDifferential = []
homeTeamSpreadResult = []
for x in range(0,len(favoriteIsHomeTeamList)):
    if favoriteIsHomeTeamList[x] == 1:
        homeTeamScoreList.append(allData.loc[x].at['Favorite_Score'])
        awayTeamScoreList.append(allData.loc[x].at['Underdog_Score'])
        if allData.loc[x].at['Spread_Margin'] > 0:
            homeTeamSpreadResult.append('W')
        elif allData.loc[x].at['Spread_Margin'] < 0:
            homeTeamSpreadResult.append('L')
        else:
            homeTeamSpreadResult.append('P')
    else:
        homeTeamScoreList.append(allData.loc[x].at['Underdog_Score'])
        awayTeamScoreList.append(allData.loc[x].at['Favorite_Score'])
        if allData.loc[x].at['Spread_Margin'] > 0:
            homeTeamSpreadResult.append('W')
        elif allData.loc[x].at['Spread_Margin'] < 0:
            homeTeamSpreadResult.append('L')
        else:
            homeTeamSpreadResult.append('P')
    homeTeamPointDifferential.append(int(homeTeamScoreList[x]) - int(awayTeamScoreList[x]))
spreadAnalysisDF = pd.DataFrame()
spreadAnalysisDF['Favorite_Score'] = allData['Favorite_Score']
spreadAnalysisDF['Underdog_Score'] = allData['Underdog_Score']
spreadAnalysisDF['Spread'] = allData['Spread'].astype('float')
spreadAnalysisDF['Spread_Margin'] = allData['Spread_Margin']
spreadAnalysisDF['Home_Team_Spread_Result'] = homeTeamSpreadResult
print(spreadAnalysisDF)
print(spreadAnalysisDF['Home_Team_Spread_Result'].value_counts())
print(spreadAnalysisDF['Home_Team_Spread_Result'].value_counts(normalize=True))
# plt.plot(spreadAnalysisDF['Spread'], spreadAnalysisDF['Spread_Margin'],'o')
bins = [1,2.4,4.5,8,11.5,15,22]
# bins = np.linspace(min(spreadAnalysisDF['Spread']), max(spreadAnalysisDF['Spread']),7)
# print(bins)
groupNames = [1,2,3,4,5,6]
spreadAnalysisDF['Spread-Binned'] = pd.cut(spreadAnalysisDF['Spread'], bins, labels=groupNames, include_lowest=True)
print(spreadAnalysisDF[['Spread','Spread-Binned']])
print(spreadAnalysisDF['Spread-Binned'].value_counts())
plt.bar(groupNames, spreadAnalysisDF['Spread-Binned'].value_counts())
plt.xlabel('Spread')
plt.ylabel('Count')
plt.title('Spread Bins')
plt.show()
counter = 1
for x in range(0,len(bins)):
    binSpreadAnalysisDF = spreadAnalysisDF.loc[spreadAnalysisDF['Spread-Binned'] == counter]
    print('Count: ', binSpreadAnalysisDF['Spread-Binned'].count(), 'Range: ', bins[counter-1], 'to ', bins[counter])
    print(binSpreadAnalysisDF['Home_Team_Spread_Result'].value_counts(normalize=True))
    counter = counter + 1
