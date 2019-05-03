# IS590PR 2019 Spring Final_Project

IS590PR Spring 2019. Top-level repository for student project forks
The detailed instructions for the Final Projects will be in the course Moodle.

## Title:
Analysis and Monte Carlo Simulation of Premier League season 2018-2019 outcome

## Team: Yang Wu(yangwu4), Siyu Liu(SelamaAshalanore6)

## Summary: 
As one of the most popular sports in Europe, even all over the world, the Premier League has become more competitive than ever. It’s very unpredictive which team would be more likely to win the championship title. By looking at a dataset consist information of 380 matches of last season and details including 42 features, this project is intended to use Monte Carlo to simulate 10,000 season outcomes to find out the likelihood/probability of every participating team to win the championship title after this on-going season.

## Hypotheses:
1. Manchester City is the most likely candidate to win the championship title.
2. Arsenal F.C. would be the least possible to be ranked within the top 4 comparing to other big six teams.
3. There is no correlation between goal scored, wins got and possession strategy spesificallly for team Manchester City.

Github repository: https://github.com/SelamaAshalanore6/Final_Project
Dataset Link: https://www.kaggle.com/zaeemnalla/premier-league#stats.csv
More dataset from:
https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/6829/Stages/15151/TeamStatistics/England-Premier-League-2017-2018
https://www.fifaindex.com/teams/fifa18_278/?league=13&order=desc


Explanation...



### Note for instructor Weible:
Please grade on the py file instead of the jupyter notebook, yet they are essentially the same thing.
If the py file simulation takes too long to run, please modify the variable 'number_seasons_to_simulate' to 100 or 10.
Even the simulation seems only to run 1000 times in the py script, in fact, one simulation contains 380 games.
