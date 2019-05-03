#590 PR final project, spring 2019

import pandas as pd
import numpy as np
from math import e
import math 
import random
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# %matplotlib inline

###Part one: pre-process datasets to create a base data frame (performance of previous season) and a fifa data frame

result = pd.read_csv('results.csv')
# result.head()
#limited result only from last season out of the 12 season records
result = result[result['season'] == '2017-2018'] 

#get a list of correct spelling of all team names
team_names = result.home_team.unique()
team_names = team_names.tolist()
# type(team_names)
team_names.sort()


home = result.groupby('home_team')['home_goals'].sum()
away = result.groupby('away_team')['away_goals'].sum()
home.sort_index()
away.sort_index()

#stats of 20 teams from last season
stats = pd.read_csv('stats.csv')
stats = stats[stats['season'] == '2017-2018']
# stats.columns

passes = stats[['team','total_pass','total_through_ball','total_long_balls','backward_pass','total_cross']]
passes['avg_pass'] = passes['total_pass'] / 38
passes.sort_values('avg_pass',ascending=False)

#data from whoscored website
whoscored = pd.read_csv('whoscored.csv')

whoscored = whoscored.drop(columns='R')
whoscored = whoscored[['Team','Possession%','Pass%']]

passes = passes.reset_index()
passes = passes.drop(columns='index')

whoscored = whoscored.replace('Tottenham','Tottenham Hotspur')
whoscored = whoscored.replace('Manchester Utd','Manchester United')
whoscored = whoscored.replace('West Ham','West Ham United')
whoscored = whoscored.replace('West Brom','West Bromwich Albion')
whoscored = whoscored.replace('Bournemouth','AFC Bournemouth')
whoscored = whoscored.replace('Newcastle Utd','Newcastle United')
whoscored = whoscored.replace('Brighton','Brighton and Hove Albion')
whoscored = whoscored.replace('Huddersfield','Huddersfield Town')
whoscored = whoscored.replace('Swansea','Swansea City')
whoscored = whoscored.replace('Stoke','Stoke City')
whoscored = whoscored.replace('Leicester','Leicester City')


possession_df = passes.merge(whoscored,left_on='team',right_on='Team')
# possession_df.head()
league_wide_avg_possession = possession_df['Possession%'].sum() / 20
# league_wide_avg_possession

stat = pd.read_csv('stats.csv')
stat = stat[stat['season'] == '2017-2018']
stat = stat[['team','goals']]
stat = stat.sort_values(by='team')
total_goals = stat['goals']
total_goals = total_goals.tolist()


base_df = pd.DataFrame({
    'Team Name': team_names,
    'Home Goals': home,
    'Away Goals': away,
    'Total Goals': total_goals
})

# base_df
base_df = base_df.reset_index(drop=True)
base_df['Home Goals Per Game'] = base_df['Home Goals'] / 19
base_df['Away Goals Per Game'] = base_df['Away Goals'] / 19

# base_df


#web scarping ATT MID DEF OVR values from fifa.index
res = requests.get('https://www.fifaindex.com/teams/fifa18_278/?league=13&order=desc')
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0] 
fifa = pd.read_html(str(table))
fifa_pl_2018 = fifa[0]

fifa_pl_2018 = fifa_pl_2018[['Name','ATT','MID','DEF','OVR']]
# fifa_pl_2018


# In[39]:


# base_df['Team Name']
#make sure all team names are coherent across different data sources
fifa_pl_2018 = fifa_pl_2018.replace('Spurs','Tottenham Hotspur')
fifa_pl_2018 = fifa_pl_2018.replace('Manchester Utd','Manchester United')
fifa_pl_2018 = fifa_pl_2018.replace('West Ham','West Ham United')
fifa_pl_2018 = fifa_pl_2018.replace('West Brom','West Bromwich Albion')
fifa_pl_2018 = fifa_pl_2018.replace('Bournemouth','AFC Bournemouth')
fifa_pl_2018 = fifa_pl_2018.replace('Newcastle Utd','Newcastle United')
fifa_pl_2018 = fifa_pl_2018.replace('Brighton','Brighton and Hove Albion')
fifa_pl_2018 = fifa_pl_2018.replace('Huddersfield','Huddersfield Town')

#merge previous season performance with FIFA values
df = base_df.merge(fifa_pl_2018,left_on='Team Name',right_on='Name')
# df.head()
df = df.drop(columns='Name')
df = df.merge(possession_df,left_on='Team Name',right_on='team')
df = df.drop(columns=['team','Team'])
#all data from last season gathered for probability calculation




avg_home_goal_per_game = df['Home Goals'].sum()/20/19
avg_away_goal_per_game = df['Away Goals'].sum()/20/19
avg_ATT = df['ATT'].sum()/20
avg_DEF = df['DEF'].sum()/20

# avg_home_goal_per_game
# avg_away_goal_per_game

names = df['Team Name'].unique().tolist()
manc = ['Manchester City']*20

formula = pd.DataFrame({
    'Home Team': manc + names,
    'Away Team': names + manc
})
formula = formula.drop([10,30])
formula = formula.reset_index()
formula = formula.drop(columns='index')

formula['Home Team Lambda'] = ''
formula['Away Team Lambda'] = ''
formula['P-Home'] = ''
formula['P-Away'] = ''
formula['Prob-Home'] = ''
formula['Prob-Away'] = ''

formula['Home passes min'] = ''
formula['Home passes max'] = ''
formula['Away passes min'] = ''
formula['Away passes max'] = ''
# formula is only the dataset illustrates Manchester City's schedule for a season

#spesify only goals from 0 to 10 are taken into consideration in this simulation
goal_range = list(range(0,11))

# goal_range
# len(goal_range)

def po(goal_range: list,factor: float):
    """
    scoring probablity of 10 different goal situations
    :param goal_range: goal range from 0 to 10 goals
    :param factor: lambda factor
    :return: probability indicator of scoring certain goals
    >>> po([1,2,3,4,5,6,7,8,9,10],float(df[df['Team Name'] == 'Manchester City']['Home Goals Per Game']))
    >>> [0.1294977942530477,0.20787803814305025,0.22246597064431697,0.17855821328030705,0.11465316852735506,0.061349502457619824,0.02813774172868277,0.011292120035852957,0.004028183170684388,0.0012932588074302512]
    """
    list = []
    factor_lambda = factor
    for goal in goal_range:    
        output = (e**(-factor_lambda))*(factor_lambda**goal) / (math.factorial(goal))
        list.append(output)
    
    return list

# float(df[df['Team Name'] == 'Manchester City']['Home Goals Per Game'])




#populate the data frame with all scoring probabilities
for index, row in formula.iterrows():

    home_team = row['Home Team']
    away_team = row['Away Team']
    
    row['Home Team Lambda'] = float(df[df['Team Name'] == home_team]['Home Goals Per Game']) * (int(df[df['Team Name'] == home_team]['ATT']) / avg_ATT) * (int(df[df['Team Name'] == away_team]['DEF']) / avg_DEF)
    row['Away Team Lambda'] = float(df[df['Team Name'] == away_team]['Away Goals Per Game']) * (int(df[df['Team Name'] == away_team]['ATT']) / avg_ATT) * (int(df[df['Team Name'] == home_team]['DEF']) / avg_DEF)

    row['P-Home'] = po(goal_range,row['Home Team Lambda']) # why row['P-Home'] is not list object?!
    row['P-Away'] = po(goal_range,row['Away Team Lambda'])

    temp_list = []
    y = row['P-Home']
    for index in range(0,len(y)):


        if index == 0:
            temp = y[index]
            temp_list.append(temp)
        else:
            temp = temp_list[index-1]
            temp += y[index]
            temp_list.append(temp)
            
    row['Prob-Home'] = temp_list

    temp_list = []
    y = row['P-Away']
    for index in range(0,len(y)):


        if index == 0:
            temp = y[index]
            temp_list.append(temp)
        else:
            temp = temp_list[index-1]
            temp += y[index]
            temp_list.append(temp)
    row['Prob-Away'] = temp_list

    row['Home passes min'] = float(df[df['Team Name'] == home_team]['avg_pass'])
    row['Home passes max'] = float(df[df['Team Name'] == home_team]['avg_pass']) / (float(df[df['Team Name'] == home_team]['Pass%']) / 100)
    row['Away passes min'] = float(df[df['Team Name'] == away_team]['avg_pass'])
    row['Away passes max'] = float(df[df['Team Name'] == away_team]['avg_pass']) / (float(df[df['Team Name'] == away_team]['Pass%']) / 100)
#formula.head()
#all probability calculated


# Test on the Lambda factor in the goal probability function:
def prob(goal: int):
    """
    get probability of scoring certain goal
    :param goal: goal number
    :return: fraction number of probability
    >>> prob(0)
    >>> 0.20315622797327135
    """
    factor_lambda = 1.59378
    output = (e**(-factor_lambda))*(factor_lambda**goal) / (math.factorial(goal))
    return output


# prob(0),prob(1),prob(2),prob(3),prob(4),prob(5),prob(6)
# prob(0),prob(1),prob(2),prob(3),prob(4),prob(5),prob(6)

#Part two: set up the simulation

# random.uniform(0,1)


# In[74]:


def simulation(dataframe: pd.DataFrame):
    """
    using the formula data frame to generate individual games of manchester city
    :param dataframe: formula data frame
    :return: lines of matches result
    >>> list_matches = simulation(formula)
    >>> len(list_matches)
    >>> 38
    """
    output = []
    for index, row in dataframe.iterrows():

        home_team = row['Home Team']
        away_team = row['Away Team']
        home_random = random.uniform(0,1)
        away_random = random.uniform(0,1)
        home_score_list = row['Prob-Home']
        away_score_list = row['Prob-Away']
        
        home_goal = 0
        away_goal = 0
#         print(len(home_score_list),len(away_score_list))
        for index in range(0,len(home_score_list)):
            if home_random >= home_score_list[index]:
                home_goal = index
        
        for index in range(0,len(away_score_list)):
            if away_random >= away_score_list[index]:
                away_goal = index
    
    
    
        print(home_team,'',home_goal,':',away_goal,'',away_team)
        temp = home_team + ' ' + str(home_goal) + ':' + str(away_goal) + ' ' + away_team
        output.append(temp)
    return output

# simulation(formula)
# if you want to simulate only focused on Manchester City for numerous seasons, run a loop for a number of times
# for i in range(0,10000):
#     simulation(formula)



fixture_schedule = pd.read_csv('fixture_schedule.csv')
fixture_schedule['Home Team Lambda'] = ''
fixture_schedule['Away Team Lambda'] = ''
fixture_schedule['P-Home'] = ''
fixture_schedule['P-Away'] = ''
fixture_schedule['Prob-Home'] = ''
fixture_schedule['Prob-Away'] = ''

fixture_schedule = fixture_schedule.rename(columns={'home_team':'Home Team','away_team':'Away Team'})
# fixture_schedule.head()

#populate probabilities into fixture schedule
def populate_lambda(input_df: pd.DataFrame):
    """
    populate the fixture_schedule data frame with probabilities
    :param input_df: fixture_schedule df
    :return: no return output, simply operations on a existed data frame, thus no test needed
    """
    for index, row in input_df.iterrows():

        home_team = row['Home Team']
        away_team = row['Away Team']

        row['Home Team Lambda'] = float(df[df['Team Name'] == home_team]['Home Goals Per Game']) * (int(df[df['Team Name'] == home_team]['ATT']) / avg_ATT) *         (int(df[df['Team Name'] == away_team]['DEF']) / avg_DEF)
        row['Away Team Lambda'] = float(df[df['Team Name'] == away_team]['Away Goals Per Game']) * (int(df[df['Team Name'] == away_team]['ATT']) / avg_ATT) *         (int(df[df['Team Name'] == home_team]['DEF']) / avg_DEF)

        row['P-Home'] = po(goal_range,row['Home Team Lambda']) # why row['P-Home'] is not list object?!
        row['P-Away'] = po(goal_range,row['Away Team Lambda'])

        temp_list = []
        y = row['P-Home']
        for index in range(0,len(y)):


            if index == 0:
                temp = y[index]
                temp_list.append(temp)
            else:
                temp = temp_list[index-1]
                temp += y[index]
                temp_list.append(temp)

        row['Prob-Home'] = temp_list

        temp_list = []
        y = row['P-Away']
        for index in range(0,len(y)):


            if index == 0:
                temp = y[index]
                temp_list.append(temp)
            else:
                temp = temp_list[index-1]
                temp += y[index]
                temp_list.append(temp)
        row['Prob-Away'] = temp_list

populate_lambda(fixture_schedule)
# fixture_schedule.head()

# simulation on a whole season according to fixture schedule
# simulation(fixture_schedule)


def simulation_store_in_df(dataframe: pd.DataFrame) ->pd.DataFrame:
    """
    based on the fixture schedule with probabilities, simulate a season
    :param dataframe: fixture schedule data frame with probabilities
    :return: data frame stored match results, not list of strings of match results
    >>> match_result_sim1 = simulation_store_in_df(fixture_schedule)
    >>> match_result_sim1.shape
    >>> (380,4)
    """
    output_df = pd.DataFrame(columns=['Home Team','Home Goal','Away Goal','Away Team'])
    i = 0
    for index, row in dataframe.iterrows():

        home_team = row['Home Team']
        away_team = row['Away Team']
        home_random = random.uniform(0,1)
        away_random = random.uniform(0,1)
        home_score_list = row['Prob-Home']
        away_score_list = row['Prob-Away']
        
        home_goal = 0
        away_goal = 0
#         print(len(home_score_list),len(away_score_list))
        for index in range(0,len(home_score_list)):
            if home_random >= home_score_list[index]:
                home_goal = index
        
        for index in range(0,len(away_score_list)):
            if away_random >= away_score_list[index]:
                away_goal = index
    
    
#         output_df['Home Team'] = home_team
#         output_df['Home Goal'] = home_goal
#         output_df['Away Goal'] = away_goal
#         output_df['Away Team'] = away_team
        output_df = output_df.append({'Home Team':home_team,'Home Goal':home_goal,'Away Goal':away_goal,
                                      'Away Team':away_team,},ignore_index=True)
        i+=1
        
    return output_df


match_result_sim1 = simulation_store_in_df(fixture_schedule)
# match_result_sim1


empty_score_table = pd.read_csv('empty_score_table(1).csv')
# empty_score_table.head()


def transform_to_score_table(dataframe: pd.DataFrame)-> pd.DataFrame:
    """
    use previous generated one season match result, transform it into a ordinary scoring table we see
    :param dataframe: previous calculated one season of matches
    :return: ordinary scoring table, with win, lose, goals, points
    >>> result_test = transform_to_score_table(match_result_sim1)
    >>> result_test.shape[0]
    >>> 20
    """
    new_dataframe = empty_score_table.copy()
    new_dataframe = new_dataframe.sort_values('team',ascending=True)
    for index, row in dataframe.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']
        home_goal = row['Home Goal']
        away_goal = row['Away Goal']
        
        if row['Home Goal'] > row['Away Goal']:
            new_dataframe.loc[new_dataframe['team'] == home_team, 'w'] += 1
            new_dataframe.loc[new_dataframe['team'] == home_team, 'pts'] += 3
            new_dataframe.loc[new_dataframe['team'] == home_team, 'gf'] += home_goal
            new_dataframe.loc[new_dataframe['team'] == home_team, 'ga'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'l'] += 1
            new_dataframe.loc[new_dataframe['team'] == away_team, 'gf'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'ga'] += home_goal
            
        elif row['Away Goal'] > row['Home Goal']:
            
            new_dataframe.loc[new_dataframe['team'] == home_team, 'l'] +=1
            new_dataframe.loc[new_dataframe['team'] == home_team, 'gf'] += home_goal
            new_dataframe.loc[new_dataframe['team'] == home_team, 'ga'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'w'] += 1
            new_dataframe.loc[new_dataframe['team'] == away_team, 'gf'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'ga'] += home_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'pts'] += 3
            
        elif row['Away Goal'] == row['Home Goal']:
            new_dataframe.loc[new_dataframe['team'] == home_team, 'pts'] +=1
            new_dataframe.loc[new_dataframe['team'] == home_team, 'gf'] += home_goal
            new_dataframe.loc[new_dataframe['team'] == home_team, 'ga'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'pts'] +=1
            new_dataframe.loc[new_dataframe['team'] == away_team, 'gf'] += away_goal
            new_dataframe.loc[new_dataframe['team'] == away_team, 'ga'] += home_goal
            
    new_dataframe['gd'] = new_dataframe['gf'] - new_dataframe['ga']
    new_dataframe = new_dataframe[['team','w','l','gf','ga','gd','pts']]
#     new_dataframe = new_dataframe.sort_values('pts',ascending=False)
    
    return new_dataframe


result_test = transform_to_score_table(match_result_sim1)
# result_test


name_list = result_test['team']
name_list = name_list.tolist()


empty_df = result_test.copy()

for col in empty_df.columns:
    empty_df[col].values[:] = 0
empty_df['team'] = ''
# an empty df similar to normal scoring table for later use of inserting number of seasons record into it
# empty_df.head()

#set numbers of simulations
number_seasons_to_simulate = 100

for i in range(0,number_seasons_to_simulate):
    each_season = simulation_store_in_df(fixture_schedule)
    each_season = transform_to_score_table(each_season)
  
    empty_df = empty_df.add(each_season)


# empty_df


def write_to_csv(times: int):
    empty_df['team'] = name_list
    empty_df['w'] = empty_df['w']/times
    empty_df['l'] = empty_df['l']/times
    empty_df['gf'] = empty_df['gf']/times
    empty_df['ga'] = empty_df['ga']/times
    empty_df['gd'] = empty_df['gd']/times
    empty_df['pts'] = empty_df['pts']/times
    empty_df.sort_values('pts',ascending=False)


    empty_df.to_csv('1000times.csv',index=False)

write_to_csv(number_seasons_to_simulate)


def simulation_store_in_df_with_possession(dataframe: pd.DataFrame) -> pd.DataFrame:
    output_df = pd.DataFrame(
        columns=['Home Team', 'Home Goal', 'Away Goal', 'Away Team', 'Home Possession', 'Away Possession'])
    i = 0
    for index, row in dataframe.iterrows():

        home_team = row['Home Team']
        away_team = row['Away Team']
        home_random = random.uniform(0, 1)
        away_random = random.uniform(0, 1)
        home_score_list = row['Prob-Home']
        away_score_list = row['Prob-Away']

        home_random_passes = random.randint(round(row['Home passes min']), round(row['Home passes max']))
        away_random_passes = random.randint(round(row['Away passes min']), round(row['Away passes max']))

        home_pos = round(home_random_passes / (home_random_passes + away_random_passes) * 100)
        away_pos = round(away_random_passes / (home_random_passes + away_random_passes) * 100)

        home_goal = 0
        away_goal = 0
        #         print(len(home_score_list),len(away_score_list))
        for index in range(0, len(home_score_list)):
            if home_random >= home_score_list[index]:
                home_goal = index

        for index in range(0, len(away_score_list)):
            if away_random >= away_score_list[index]:
                away_goal = index

        #         output_df['Home Team'] = home_team
        #         output_df['Home Goal'] = home_goal
        #         output_df['Away Goal'] = away_goal
        #         output_df['Away Team'] = away_team
        output_df = output_df.append({'Home Team': home_team, 'Home Goal': home_goal, 'Away Goal': away_goal,
                                      'Away Team': away_team, 'Home Possession': home_pos, 'Away Possession': away_pos},
                                     ignore_index=True)
        i += 1

    return output_df



list_wins = []
list_pos = []
list_goals = []
for i in range(0,1000):
    temp_df = simulation_store_in_df_with_possession(formula)
    win_match = 0
    goals = 0
    for index, row in temp_df.iterrows():
        if row['Home Team'] == 'Manchester City':
            goals += row['Home Goal']
            if row['Home Goal'] > row['Away Goal']:
                win_match += 1
        elif row['Away Team'] == 'Manchester City':
            goals += row['Away Goal']
            if row['Away Goal'] > row['Home Goal']:
                win_match += 1
    top_19 = temp_df.iloc[1:19]
    bottom_19 = temp_df.iloc[20:]
    avg_pos = (top_19['Home Possession'].sum() + bottom_19['Away Possession'].sum()) / 38
    list_wins.append(win_match)
    list_pos.append(avg_pos)
    list_goals.append(goals)

plt.scatter(list_wins,list_pos)
plt.savefig('winspos.png')
plt.scatter(list_goals,list_pos)
plt.savefig('goalspos.png')
