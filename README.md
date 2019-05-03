# IS590PR 2019 Spring Final_Project

IS590PR Spring 2019. Top-level repository for student project forks
The detailed instructions for the Final Projects will be in the course Moodle.

## Title:
Analysis and Monte Carlo Simulation of Premier League season 2018-2019 outcome

## Team: 
Yang Wu(yangwu4), Siyu Liu(SelamaAshalanore6)

## Summary of objective: 
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

## Conclusion:
In our simulation, based on visualizations plotted and data frame results in the program:
1. Manchester City is indeed the most likely condidate for winning the title.
2. Arsenal is not the weakest team among the 'top 6' of the BPL, it's simulated to be in the top 4 position to qualify the UEFA Championship League.
3. There's in fact no correlations between wins/goals and team possession strategy.

### Note for instructor Weible:
Please grade on the py file instead of the jupyter notebook, yet they are essentially the same thing.
If the py file simulation takes too long to run, please modify the variable 'number_seasons_to_simulate' to 100 or 10.
Even the simulation seems only to run 1000 times in the py script, in fact, one simulation contains 380 games.

Although we choose only 2017-18 season to simulate results in Premier League for next season, our simulation only functions with fixed league teams. The Premier League has a rule called ‘relegation’, which means the last three ranked teams would be relegated to the inferior league called EFL Championship and three other teams that ranked top three in EFL Championship will be promoted to Premier League, so there are always changes in the twenty teams in Premier League. 
Given your suggestion, we cannot simulate a new season based on three previous season combined; one reason is the teams are different, addtionally, we use the model Poisson distribution to calculate the factor called lambda, and we scrap numbers from FIFA for per team, which are attack score, defense score and overall, and they can be called as the ability numbers of teams, which are various per year. If we choose multiple years, we need to scrap the ability numbers of teams in terms of years. Since teams are all different in a season, we cannot calculate the average FIFA strength. Besides, we use ‘home/away goals per game’ to calculate this lambda, for one team, if the opposite teams changed, the performance and goals would also change, so the number of average goals would be meaningless.
As for the suggestion to simulate 17-18 season based on 16-17 results and fifa numbers, that's exactly the same as our model which does not valiadate the model itself. Our team decided to add a new feature of ball possession into the simulation and analyze the relationship between wins/goals and possession rate which was always our first intention of doing this simulation in the first place.


